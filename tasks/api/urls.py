from rest_framework.routers import DefaultRouter

from .views import AssignmentViewSet, AssignmentSubmissionViewSet, QuestionBankViewSet, QuestionViewSet, AnswerOptionViewSet, TestViewSet, TestQuestionViewSet, TestAttemptViewSet, StudentAnswerViewSet

router = DefaultRouter()
router.register(r"assignments", AssignmentViewSet, basename="assignments")
router.register(r"submissions", AssignmentSubmissionViewSet, basename="submissions")
router.register(r"question-banks", QuestionBankViewSet, basename="question-banks")
router.register(r"questions", QuestionViewSet, basename="questions")
router.register(r"answer-options", AnswerOptionViewSet, basename="answer-options")
router.register(r"tests", TestViewSet, basename="tests")
router.register(r"test-questions", TestQuestionViewSet, basename="test-questions")
router.register(r"test-attempts", TestAttemptViewSet, basename="test-attempts")
router.register(r"student-answers", StudentAnswerViewSet, basename="student-answers")

urlpatterns = router.urls
