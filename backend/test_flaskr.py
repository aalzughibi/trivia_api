import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test1"#trivia_test
        self.database_path = "postgres://{}/{}".format('postgres:1234@127.0.0.1:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories(self): #done
        x = self.client().get('/categories')
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_paginated_question(self): #done
        x = self.client().get('/questions?page=1')
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["current_category"]))

    def test_get_paginated_question_404(self):#done
        x = self.client().get('/questions?page=1000000')
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_delete_question(self):#done
        x = self.client().delete('/questions/2')
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_404(self):#done
        x = self.client().delete('/questions/100000000')
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_addQuestion(self):#done
        insert_data = {
            'question': 'If A and B together can complete a piece of work in 15 days and B alone in 20 days, in how many days can A alone complete the work?',
            'answer': '60',
            'category': 1,
            'difficulty': 1
        }
        x = self.client().post('/questions', json=insert_data)
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_addQuestion_422(self):#done
        insert_data = {
            'question': 'test',
            'answer': 'test'
        }
        x = self.client().post('/questions', json=insert_data)
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    def test_search_questions(self):
        insert_data = {
            'searchTerm': 'x',
        }
        x = self.client().post('/questions', json=insert_data)
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["count"])

    def test_search_questions_422(self):
        insert_data = {
            'searchTerm': None,
        }
        x = self.client().post('/questions', json=insert_data)
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_search_questions_422(self):
        insert_data = {
            'searchTerm': None,
        }
        x = self.client().post('/questions', json=insert_data)
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_getQuestionByCategory(self):
        x = self.client().get('/categories/1/questions')
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))

    def test_getQuestionByCategory_404(self):
        x = self.client().get('/categories/1000/questions')
        data = json.loads(x.data)
        self.assertEqual(x.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")

    def test_play_quiz(self):
        insert_data = {
            'previous_questions': [],
            'quiz_category': {'id':1}
        }
        res = self.client().post('/quizzes', json=insert_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_play_quiz_422(self):
        insert_data = {}
        res = self.client().post('/quizzes', json=insert_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    
    unittest.main()