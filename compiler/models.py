from django.db import models
import bcrypt
from typing import Tuple, Optional, Dict
import os
from dotenv import load_dotenv
import jwt
import datetime
import subprocess
import time

from .errors import *
from .utils.chore import is_valid_email
from .utils.hash import hash_password, verify_password


load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_MAX_TIMEDELTA = datetime.timedelta(minutes=30)

if not JWT_SECRET_KEY:
    raise("Please create an Environment Variable named JWT_SECRET_KEY")


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
 
    def __str__(self) -> str:
        return str(self.username)

    @classmethod
    def create_user(cls, name :str, username :str, email :str, password :str) -> Tuple[int, str, Optional["User"]]:
        if not all([name, username, email, password]):
            return (400, IncompleteData, None)

        if User.objects.filter(username=username).exists():
            return (403, UserExists, None)

        if not is_valid_email(email):
            return (403, InvalidEmail, None)

        hashed_password = hash_password(password)
        user = cls(name=name, username=username, email=email, password_hash=hashed_password)
        user.save()

        return(200,UserCreated, user)

    @classmethod
    def verify_user(cls, uname :str, password :str) -> Tuple[int, str, Optional["User"]]:
        if not all([uname, password]):
            return (400, IncompleteData, None)
        
        user = cls.objects.filter(username=uname).first()
        if not user:
            return (404, UserNotExists, None)

        auth = verify_password(password=password, hashed_password=user.password_hash)

        if auth:
            return (200, LoggedIn, user)
        else:
            return (401, InvalidCredentials, None)

    def generateJWT(self) -> str:
        expiration_time = datetime.datetime.utcnow() + JWT_MAX_TIMEDELTA

        payload = {
            'username': self.username,
            'email': self.email,
            'exp': expiration_time
        }

        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

        return token

    def getUserFromJWT(token :str) -> Tuple[bool, str, Optional["User"]]:
        if not token:
            return (False, NoToken, None)
            
        try:
            decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])

            username = decoded_payload.get('username')
            email = decoded_payload.get('email')

            user = User.objects.filter(username=username).first() 
            if user and user.email == email:
                return (True, ValidToken, user)
            return (False, UserNotExists, None)

        except jwt.ExpiredSignatureError:
            return (False, ExpiredToken, None)
        except jwt.InvalidTokenError:
            return (False, InvalidToken, None)
        except Exception as e:
            return (False, str(e), None)
        

class CodeHandler():
    def __init__(self, code :str, language :str) -> None:
        if not all([code, language]):
            return
        if language not in ['cpp','java','python']:
            return

        self.__code = code
        self.__language = language
        self.__output = None
        self.__error = None
        self.__runtime = None
        self.__suggestion = None
        self.__user_input = None

    def getCode(self) -> str:
        return self.__code

    def updateCode(self, code :str) -> bool:
        if code:
            self.__code = code
            return True
        return False

    def getLanguage(self) -> str:
        return self.__language

    def updateLanguage(self, language :str) -> bool:
        if language in ['cpp','java','python']:
            self.__language = language
            return True
        return False

    def getOutput(self) -> Optional[str]:
        return self.__output

    def getError(self) -> Optional[str]:
        return self.__error

    def getRuntime(self) -> Optional[str]:
        return self.__runtime

    def getSuggestion(self) -> Optional[str]:
        return self.__suggestion

    def setUserInput(self, input :str):
        self.__user_input = input

    def execute(self) -> None:
        try:
            temp_dir = './temp_code'
            os.makedirs(temp_dir, exist_ok=True)
            if self.__language == 'python':
                filename = f'{temp_dir}/script.py'
                with open(filename, 'w') as file:
                    file.write(self.__code)
                docker_image = 'python:3.10'
                command = f'python /code/script.py'

            elif self.__language == 'cpp':
                filename = f'{temp_dir}/program.cpp'
                with open(filename, 'w') as file:
                    file.write(self.__code)
                docker_image = 'gcc:latest'
                command = f'g++ /code/program.cpp -o /code/program.out && /code/program.out'

            elif self.__language == 'java':
                filename = f'{temp_dir}/Program.java'
                with open(filename, 'w') as file:
                    file.write(self.__code)
                docker_image = 'openjdk:latest'
                command = f'javac /code/Program.java && java -cp /code Program'

            else:
                self.__error = "Unsupported language"
                return

            docker_command = [
                'docker', 'run', '--rm', '-i',
                '--cpus', '1', '--memory', '128m', '--memory-swap', '128m',
                '-v', f'{os.path.abspath(temp_dir)}:/code',
                '-w', '/code',
                docker_image,
                'sh', '-c', command
            ]

            start_time = time.time()
            result = subprocess.run(
                docker_command,
                input=self.__user_input,
                capture_output=True,
                text=True,
                timeout=3  # Timeout for the Docker container
            )
            end_time = time.time()

            self.__runtime = f"{end_time - start_time:.3f} seconds"
            self.__output = result.stdout
            self.__error = result.stderr
        except subprocess.TimeoutExpired:
            self.__error = "Time Limit Exceeded"
        except subprocess.CalledProcessError as e:
            if "memory" in str(e):
                self.__error = "Memory Limit Exceeded"
            else:
                self.__error = str(e)
        except Exception as e:
            self.__error = str(e)   

class Problem(models.Model):
    title = models.CharField(max_length=255)
    statement = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    try_count = models.IntegerField(default=0)
    solve_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def getProblemID(self) -> int:
        return self.id

    def getCreator(self) -> str:
        return self.creator.username

    def addTestCase(self, input_data: str, expected_output :str) -> bool:
        if not all([input_data, expected_output]):
            return False
        test_case = TestCase(problem=self, input_data=input_data, expected_output=expected_output)
        self.testcase_count += 1
        self.save()
        test_case.save()
        return True

    @classmethod
    def createProblem(cls, title: str, statement: str, creator: User, testcases: Dict[str,str]) -> Tuple[int, str]:
        if not all([title, statement, User, testcases]):
            return (400, IncompleteData)
        
        problem = cls(title=title, statement=statement, creator=creator)
        problem.save()
        for input_data, expected_output in testcases.items():
            problem.addTestCase(input_data, expected_output)

        return (200, ProblemCreated)

    def solve(self, code :CodeHandler, firstSubmission: bool) -> Tuple[bool, int, str]:
        passed_tests = 0
        all_test_cases = self.test_cases.all()
        isSucceed = True
        if firstSubmission:
            self.try_count += 1
            self.save()
        message = NoOperation
        for test in all_test_cases:
            isSucceed, message = test.testCode(code)
            if not isSucceed:
                return (isSucceed, passed_tests, message)
            passed_tests += 1
        if firstSubmission:
            self.solve_count += 1
            self.save()
        return (isSucceed, passed_tests, message)

class Solution(models.Model):
    code = models.TextField()
    solver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solutions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='solutions')
    
class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()

    def setInput(self, test_input :str) -> bool:
        if not test_input:
            return False
        self.input_data = test_input
        return True

    def setExcpectedOutput(self, output :str) -> bool:
        if not output:
            return False
        self.expected_output = output
        return True

    def testCode(self, code :CodeHandler) -> Tuple[bool, str]:
        code.setUserInput(self.input_data)
        try:
            code.execute()
        except Exception as e:
            return (False, str(e))
        if code.getOutput() == self.expected_output:
            return (True, "success")
        else:
            result = f"Input:\n{self.input_data};\n\nOutput:\n{code.getOutput()}\n\nExpected Output:\n{self.expected_output}"
            return (False, result)

