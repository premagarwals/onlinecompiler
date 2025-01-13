from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer, ProblemSerializer, TestCaseSerializer, SolutionSerializer
from .models import Solution, User, CodeHandler, Problem, TestCase, Solution
from .errors import *

### Test Endpoints

@api_view(['GET'])
def Welcome(request):
    message = {"status_code": 200, "status_message": "api is up", "message": "Hello from AxG!"}
    return Response(message)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all() 
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProblems(request):
    problems = Problem.objects.all() 
    serializer = ProblemSerializer(problems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTestcases(request):
    testcases = TestCase.objects.all() 
    serializer = TestCaseSerializer(testcases, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSolutions(request):
    solutions = Solution.objects.all() 
    serializer = SolutionSerializer(solutions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def decodeJWT(request):
    message = {"status": 500, "message": NoOperation}

    token = request.data.get("jwt")

    success, response, user = User.getUserFromJWT(token)
    message["message"] = response

    if not success:
        message["status"] = 500
        return Response(message)
    else:
        message["status"] = 200
        message["user"] = UserSerializer(user).data
        return Response(message)

    return Response(message)

### Primary Endpoints

@api_view(['POST'])
def signup(request):
    message = {"status": 500, "message": NoOperation}

    name = request.data.get("name")
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    
    status, response, user = User.create_user(name=name, username=username, email=email, password=password)

    message["status"] = status
    message["message"] = response

    if status == 200:
        message["user"] = UserSerializer(user).data
    else:
        return Response(message)

    jwt_token = user.generateJWT()
    message["jwt"] = jwt_token

    return Response(message)

@api_view(['POST'])
def login(request):
    message = {"status": 500, "message": NoOperation}

    username = request.data.get("username")
    password = request.data.get("password")

    status, response, user = User.verify_user(uname=username, password=password)

    message["status"] = status
    message["message"] = response

    if status == 200:
        message["user"] = UserSerializer(user).data
    else:
        return Response(message)

    jwt_token = user.generateJWT()
    message["jwt"] = jwt_token

    return Response(message)

@api_view(['POST'])
def coderunner(request):
    message = {"status": 500, "message": NoOperation}

    code_data = request.data.get("code")
    user_input = request.data.get("user_input")
    language = request.data.get("language")

    if not all([code_data, language]):
        message["status"] = 400
        message["message"] = IncompleteData
        return Response(message)

    code = CodeHandler(code=code_data, language=language)

    if user_input:
        code.setUserInput(user_input)

    try:
        code.execute()
    except Exception as e:
        message["status"] = 500
        message["message"] = str(e)
        return Response(message)

    message["status"] = 200
    message["message"] = code.getSuggestion()
    message["output"] = code.getOutput()
    message["error"] = code.getError()
    message["runtime"] = code.getRuntime()

    return Response(message)

@api_view(['POST'])
def addproblem(request):
    message={"status": 500, "message": NoOperation}
    title = request.data.get("title")
    statement = request.data.get("statement")
    jwt = request.data.get("jwt")
    testcases = request.data.get("testcases")
    is_valid, message["message"], creator= User.getUserFromJWT(jwt)
    if (not is_valid):
        return Response(message)
    message["status"],message["message"] = Problem.createProblem(statement=statement, creator=creator, testcases=testcases,title=title)
    return Response(message)

@api_view(['POST'])
def testcode(request):
    message = {"status": 500, "message": NoOperation}
    problem_id = request.data.get("problem_id")
    problem = Problem.objects.filter(id=problem_id).first()
    code_data = request.data.get("code")
    language = request.data.get("language")
    code = CodeHandler(code=code_data, language=language)
    jwt = request.data.get("jwt")
    is_valid, message["message"], solver = User.getUserFromJWT(jwt)
    firstSubmission = not solver.solutions.filter(problem=problem).exists()
    if (not is_valid):
        return Response(message)
    isSucceed, passed_tests, message["message"] = problem.solve(code, firstSubmission)
    if (isSucceed):
        message["message"]="passed_testcases: "+f"{passed_tests}"
        solution = Solution(code=code_data,solver=solver,problem=problem)
        solution.save()
    else:
        message["message"]=f"Sorry!! OVER FOR YOU, {passed_tests}   "+message["message"]

    return Response(message)
