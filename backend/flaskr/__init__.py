import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app,resources={r"/api/*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_req(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods = ['GET'])
  def get_all_categories():
    # if True:
    #   if True:
    #     c  =  Category(type = 'Science')
    #     c.insert()
    #     c  =  Category(type = 'Art')
    #     c.insert()
    #     c  =  Category(type = 'Geography')
    #     c.insert()
    #     c  =  Category(type = 'History')
    #     c.insert()
    #     c  =  Category(type = 'Entertainment')
    #     c.insert()
    #     c  =  Category(type = 'Sports')
    #     c.insert()
    #     ###############################################
    #     q = Question(question = "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",answer = 'Maya Angelou',category =2,difficulty=4)
    #     q.insert()
    #     q = Question(question = "Who invented Peanut Butter?",answer = 'George Washington Carver',category =2,difficulty=4)
    #     q.insert()

    #     q = Question(question = "What is the largest lake in Africa?",answer = 'Lake Victoria',category =2,difficulty=3)
    #     q.insert()
    #     q = Question(question = "In which royal palace would you find the Hall of Mirrors?",answer = 'The Palace of Versailles',category =3,difficulty=3)
    #     q.insert()
    #     q = Question(question = "The Taj Mahal is located in which Indian city?",answer = 'Agra',category =2,difficulty=3)
    #     q.insert()
    #     q = Question(question = "La Giaconda is better known as what?",answer = 'Mona Lisa',category =3,difficulty=2)
    #     q.insert()
    #     q = Question(question = "How many paintings did Van Gogh sell in his lifetime?",answer = 'one',category =4,difficulty=2)
    #     q.insert()
    #     q = Question(question = "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",answer = 'Jackson Pollock',category =2,difficulty=2)
    #     q.insert()
    #     q = Question(question = "What is the heaviest organ in the human body?",answer = 'The Liver',category =4,difficulty=1)
    #     q.insert()
    #     q = Question(question = "Who discovered penicillin?",answer = 'Alexander Fleming',category =3,difficulty=1)
    #     q.insert()
    #     q = Question(question = "Hematology is a branch of medicine involving the study of what?",answer = 'Blood',category =4,difficulty=1)
    #     q.insert()
    #     q = Question(question = "Which dung beetle was worshipped by the ancient Egyptians?",answer = 'Scarab',category =4,difficulty=4)
    #     q.insert()
    categories = Category.query.order_by('id').all()
    current_category = {}

    for i in categories:
      current_category[i.id] = i.type
    
    if len(current_category) ==0:
      abort(404)
    return jsonify({
        'success':True,
        'category':current_category
    })
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  def pageinate(request,selection):
    page = request.args.get('page',1,type=int)
    start = (page-1)* QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions
  # ##### ##### ##### ##### ##### ##### #####
  @app.route('/questions',methods = ['GET'])
  def get_all_question():
    question = Question.query.order_by('id').all()
    current_question = pageinate(request,question)
    if len(current_question) ==0:
      abort(404)
    category = Category.query.order_by('id').all()
    category = [c.format() for c in category]
    return jsonify({
      'success':True,
      'question':current_question,
      'total_question':Question.query.count(),
      'Category':category})
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 
  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods = ['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
      abort(404)
    try:
      question.delete()
      return jsonify({
        'success':True,
        'id':question.id
        })
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.
  
  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods = ['POST'])
  def addQuestion_Search_question():

    questionData = request.get_json()
    if questionData.get('search_term') is None:
      question = questionData.get('question')
      question_answer = questionData.get('answer')
      question_category  = questionData.get('category')
      question_difficulty = questionData.get('difficulty')

      if question is None or question_answer is None or question_category is None or question_difficulty is None:
        abort(422)
      try:
        ques = Question(question = question,answer = question_answer, category = question_category, difficulty = question_difficulty)
        ques.insert()

        return jsonify({
        'success':True,
        'question_id_created':ques.id,
        'total_question':Question.query.count()
       })
      except:
       abort(422)

    else:
      search_term = questionData.get('search_term')
      try:
        if search_term is None:
         abort(422)
        questionDataList  = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
        qdlCount = len(questionDataList)
        if qdlCount == 0 :
          abort(404)
        questionDataList = [qdl.format() for qdl in questionDataList]
        return jsonify({
        'success':True,
        'question':questionDataList,
        'count':qdlCount
        })
      except:
        abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # @app.route('/questions',methods = ['POST'])
  # def search_for_question():

  # # query.filter(Artist.name.like('%'+dataSearch+'%'))
  #   dataSearch = request.get_json()
  #   search_term = dataSearch.get('search_term')
  #   try:
  #     if search_term is None:
  #       abort(422)
  #     questionDataList  = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
  #     qdlCount = len(questionDataList)
  #     if qdlCount == 0 :
  #       abort(404)
  #     questionDataList = [qdl.format() for qdl in questionDataList]
  #     return jsonify({
  #       'success':True,
  #       'question':questionDataList,
  #       'count':qdlCount
  #     })
  #   except:
  #     abort(422)
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions',methods = ['GET'])
  def getQuestionByCategory(category_id):
    category = Category.query.get(category_id)
    if category is None:
      abort(404)
    question = Question.query.filter_by(category = category.id).order_by('id').all()
    question = [ques.format() for ques in question]
    return jsonify({
      'success':True,
      'questions':question
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 
  
  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods = ['POST'])
  def play_quiz():
    try:
      body = request.get_json()
      previous_questions = body.get('previous_questions',[])
      category = body.get('category')
      if category is None:
        abort(422)
      questions = Question.query.filter_by(category = category).order_by('id').all()
      questions = [ques.format() for ques in questions if ques not in previous_questions]
      questions = random.choice(questions)
      return jsonify({
        'success':True,
        'question':questions
      })
    except:
      abort(422)
    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
      }), 422
  
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400
  return app


    