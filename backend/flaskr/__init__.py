import os
from flask import Flask, request, abort, jsonify,render_template
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
  @app.route('/')
  def index():
    return render_template('index.html')
  @app.route('/categories', methods = ['GET'])
  def get_all_categories():
   
    categories = Category.query.order_by('id').all()
    current_category = {}

    for i in categories:
      current_category[i.id] = i.type
    
    if len(current_category) ==0:
      abort(404)
    return jsonify({
        'success':True,
        'categories':current_category
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
  def paginate_questions(request,selection):
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE
    formatted_selection = [sel.format() for sel in selection]
    return formatted_selection[start:end]

  # ##### ##### ##### ##### ##### ##### #####
  @app.route('/questions',methods = ['GET'])
  def get_all_question():
    questions = Question.query.order_by('id').all()
    if len(questions) == 0:
      abort(404)
    questions = paginate_questions(request,questions)
    categories = Category.query.order_by('id').all()
    formatted_categories = {}
    for category in categories:
      formatted_categories[category.id] = category.type
    total_question = Question.query.count()
    current_category = []
    for i in questions:
      if i['category'] in current_category:
        continue
      else:
        current_category.append(i['category'])
    
    
    return jsonify({
            'success': True,
            'questions': questions,
            'total_questions': total_question,
            'categories': formatted_categories,
            'current_category': current_category
        })
  
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
    if questionData.get('searchTerm'):
      search_term = questionData.get('searchTerm')
      try:
        if search_term is None:
         abort(422)
        questionDataList  = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
        qdlCount = len(questionDataList)
        questionDataList = [qdl.format() for qdl in questionDataList]
        return jsonify({
        'success':True,
        'questions':questionDataList,
        'count':qdlCount
        })
      except:
        abort(422)

    else:
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
      
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
 
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
      previous_questions = body.get('previous_questions')
      category = body.get('quiz_category')
      if category['id'] ==0:
        question = Question.query.order_by('id').all()
        rQuestion =[]
        for q in question:
          if q.id in previous_questions:
            continue
          else:
            rQuestion.append(q)
          RandomChoice = random.choice(rQuestion)
        return jsonify({
          'success':True,
          'question':RandomChoice.format()
        })
      else:
        categoryData = Category.query.get(category['id'])
        if categoryData is None:
          abort(404)
        question = Question.query.filter_by(category = category['id']).order_by('id').all()
        rQuestion = []
        for i in question:
          if i.id in previous_questions:
            continue
          else:
            rQuestion.append(i)
          RandomChoice = random.choice(rQuestion)
          # rQuestion[random.randint(0,len(rQuestion)-1)].format()
        return jsonify({
          'success':True,
          'question':RandomChoice.format()
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


    