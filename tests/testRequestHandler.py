from ppp_cas.requesthandler import RequestHandler
from ppp_datamodel.communication import Request
from ppp_datamodel.resource import Resource
from ppp_datamodel.sentence import Sentence
from unittest import TestCase

class TestRequestHandler(TestCase):

    def testNoMath(self):
        testCases=[('What is the birth date of the president of the United States?', 0), 
                   ('What is the birth date of George Washington?', 0),
                   ('Who is the director of \"Pulp Fiction\"?', 0),
                   ('Who is the president of France?', 0),
                   ('What is the capital of Australia?', 0),
                   ('Who is the author of \"Foundation\"?', 0),
                  ]
        for (expr, res) in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(len(handler.answer()), res)
        self.assertEqual(len(RequestHandler(Request(0, 'math', Resource(''))).answer()), 0)
                  
    def testMath(self):
        testCases=[('5+7', 1),
                   ('2^42', 1),
                   ('sqrt((42)**(pi))', 1),
                   ('diff(x**2,x)', 1),
                   ('Solve[x^2==1, x]', 1),
                   ('C(3.7,1.3)', 1),
                   ('lcm(n,m)hcf(n,m)', 1),
                   ('integrate(exp(-x**2), x, -infty, infty)', 1),
                   ('sqrt(2)', 1)
                  ]
        for (expr, res) in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(len(handler.answer()), res)
                  
    def testTree(self):
        testCases=[('5+7', '12'),
                   ('2^42', '4398046511104'),
                   ('sqrt((42)**(pi))', '42^{\\frac{\pi}{2}}'),
                   ('diff(x**2,x)', '2 x'),
                   ('Solve[x^2==1, x]', '\left [ \left ( -1\\right ), \quad \left ( 1\\right )\\right ]'),
                   ('C(3.7,1.3)', '4.43659695748368'),
                   ('lcm(n,m)hcf(n,m)', 'm n'),
                   ('integrate(exp(-x**2), x, -infty, infty)', '\\sqrt{\\pi}'),
                   ('sqrt(2)', '\\sqrt{2}')
                  ]
        for (expr, res) in testCases:
            handler = RequestHandler(Request(0, 'math', Sentence(expr)))
            self.assertEqual(handler.answer()[0].tree, Resource(res, value_type='math-latex'))