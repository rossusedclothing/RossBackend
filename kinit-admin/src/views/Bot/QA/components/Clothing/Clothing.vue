<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-gray-800"
            >问答配置
            <button class="btn" @click="fetchQuestionList">⭕️</button>
          </h1>
          <button
            @click="openQuestionForm"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            新增问题
          </button>
        </div>

        <!-- 问题列表 -->
        <div class="space-y-4">
          <div
            v-for="question in questions"
            :key="question.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex justify-between items-start mb-3">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">
                  问题 #{{ question.id }} {{ question.question }}
                </h3>
                <p class="text-gray-600">{{ question.question }}</p>
              </div>
              <div class="flex space-x-2 ml-4">
                <button
                  @click="editQuestion(question)"
                  class="text-blue-500 hover:text-blue-700 px-3 py-1 rounded"
                >
                  编辑
                </button>
                <button
                  @click="deleteQuestion(question.id)"
                  class="text-red-500 hover:text-red-700 px-3 py-1 rounded"
                >
                  删除
                </button>
                <button
                  @click="toggleAnswers(question.id)"
                  class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded transition-colors"
                >
                  {{ expandedQuestions.has(question.id) ? '收起答案' : '查看答案' }}
                </button>
              </div>
            </div>

            <!-- 答案列表 -->
            <div
              v-if="expandedQuestions.has(question.id)"
              class="mt-4 pl-4 border-l-2 border-blue-200"
            >
              <div class="flex justify-between items-center mb-3">
                <h4 class="text-md font-medium text-gray-700">相关答案</h4>
                <button
                  @click="openAnswerForm(question.id)"
                  class="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-sm transition-colors"
                >
                  新增答案
                </button>
              </div>

              <div class="space-y-2">
                <div
                  v-for="answer in getAnswersByQuestionId(question.id)"
                  :key="answer.id"
                  class="bg-gray-50 p-3 rounded border"
                >
                  <div class="flex justify-between items-start">
                    <div class="flex-1">
                      <p class="text-gray-800 mb-1">{{ answer.answer }}</p>
                      <p v-if="answer.next_question" class="text-sm text-blue-600">
                        → 跳转到问题 #{{ answer.next_question }}:
                        {{ getQuestionById(answer.next_question)?.question }}
                      </p>
                    </div>
                    <div class="flex space-x-2 ml-4">
                      <button
                        @click="editAnswer(answer)"
                        class="text-blue-500 hover:text-blue-700 text-sm px-2 py-1 rounded"
                      >
                        编辑
                      </button>
                      <button
                        @click="deleteAnswer(answer.id)"
                        class="text-red-500 hover:text-red-700 text-sm px-2 py-1 rounded"
                      >
                        删除
                      </button>
                    </div>
                  </div>
                </div>

                <div
                  v-if="getAnswersByQuestionId(question.id).length === 0"
                  class="text-gray-500 text-center py-4"
                >
                  暂无答案
                </div>
              </div>
            </div>
          </div>

          <div v-if="questions.length === 0" class="text-center py-8 text-gray-500">
            暂无问题，点击上方按钮添加第一个问题
          </div>
        </div>

        <!-- 问题流程图 -->
        <div v-if="questions.length > 0" class="mt-8 bg-gray-50 p-4 rounded-lg">
          <h3 class="text-lg font-semibold mb-4 text-gray-800">问题流程图</h3>
          <div class="space-y-2">
            <div v-for="question in questions" :key="question.id" class="text-sm">
              <span class="font-medium text-blue-600"
                >问题 #{{ question.id }} {{ question.question }}</span
              >
              <div class="ml-4 mt-1">
                <div
                  v-for="answer in getAnswersByQuestionId(question.id)"
                  :key="answer.id"
                  class="text-gray-600"
                >
                  "{{ answer.answer }}"
                  <span v-if="answer.next_question" class="text-green-600">
                    → 问题 #{{ answer.next_question }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 问题表单模态框 -->
    <div
      v-if="showQuestionForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h2 class="text-xl font-bold mb-4 text-gray-800">
          {{ editingQuestion ? '编辑问题' : '新增问题' }}
        </h2>
        <form @submit.prevent="saveQuestion">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">问题内容</label>
            <textarea
              v-model="questionForm.question"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows="4"
              placeholder="请输入问题内容..."
              required
            ></textarea>
          </div>
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="closeQuestionForm"
              class="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              {{ editingQuestion ? '更新' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 答案表单模态框 -->
    <div
      v-if="showAnswerForm"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h2 class="text-xl font-bold mb-4 text-gray-800">
          {{ editingAnswer ? '编辑答案' : '新增答案' }}
        </h2>
        <form @submit.prevent="saveAnswer">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">答案内容</label>
            <textarea
              v-model="answerForm.answer"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              rows="3"
              placeholder="请输入答案内容..."
              required
            ></textarea>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">下一个问题（可选）</label>
            <select
              v-model="answerForm.next_question"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="">无跳转</option>
              <option v-for="q in questions" :key="q.id" :value="q.id">
                问题 #{{ q.id }}: {{ q.question.substring(0, 50)
                }}{{ q.question.length > 50 ? '...' : '' }}
              </option>
            </select>
          </div>
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              @click="closeAnswerForm"
              class="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
            >
              {{ editingAnswer ? '更新' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  getQuestionListApi,
  delQuestionApi,
  addQuestionListApi,
  putQuestionListApi,
  getAnswerListApi,
  addAnswerListApi,
  putAnswerListApi,
  delAnswerListApi
} from '@/api/bot/qa/questiong'
import { ElTabs, ElTabPane } from 'element-plus'

const activeName = ref('服装')

// 数据状态
const questions = ref([
  { id: 1, question: '您对我们的产品满意吗？' },
  { id: 2, question: '您希望我们改进哪些方面？' },
  { id: 3, question: '您会推荐给朋友吗？' }
])

const answers = ref([
  { id: 1, question_id: 1, answer: '非常满意', next_question: 3 },
  { id: 2, question_id: 1, answer: '一般满意', next_question: 2 },
  { id: 3, question_id: 1, answer: '不满意', next_question: 2 },
  { id: 4, question_id: 2, answer: '价格方面', next_question: null },
  { id: 5, question_id: 2, answer: '功能方面', next_question: null },
  { id: 6, question_id: 3, answer: '会推荐', next_question: null },
  { id: 7, question_id: 3, answer: '不会推荐', next_question: null }
])

// UI状态
const showQuestionForm = ref(false)
const showAnswerForm = ref(false)
const expandedQuestions = ref(new Set())
const editingQuestion = ref(null)
const editingAnswer = ref(null)

// 表单数据
const questionForm = reactive({
  question: ''
})

const answerForm = reactive({
  question_id: null,
  answer: '',
  next_question: ''
})

onMounted(() => {
  fetchQuestionList()
})

const fetchQuestionList = async () => {
  const res = await getQuestionListApi()
  if (res.code == 200 && res.data) {
    questions.value = res.data
    const ansRes = await getAnswerListApi()
    if (ansRes.code == 200 && ansRes.data) {
      answers.value = ansRes.data
    } else {
      answers.value = []
    }
  } else {
    return []
  }
}

// 计算属性
const nextQuestionId = computed(() => {
  return questions.value.length > 0 ? Math.max(...questions.value.map((q) => q.id)) + 1 : 1
})

const nextAnswerId = computed(() => {
  return answers.value.length > 0 ? Math.max(...answers.value.map((a) => a.id)) + 1 : 1
})

// 工具方法
function getAnswersByQuestionId(questionId) {
  return answers.value.filter((answer) => answer.question_id === questionId)
}

function getQuestionById(questionId) {
  return questions.value.find((q) => q.id === questionId)
}

// 问题相关方法
function openQuestionForm() {
  resetQuestionForm()
  showQuestionForm.value = true
}

function closeQuestionForm() {
  showQuestionForm.value = false
  editingQuestion.value = null
  resetQuestionForm()
}

function resetQuestionForm() {
  questionForm.question = ''
}

function editQuestion(question) {
  editingQuestion.value = question
  questionForm.question = question.question
  showQuestionForm.value = true
}

function saveQuestion() {
  if (editingQuestion.value) {
    // 更新问题
    editingQuestion.value.question = questionForm.question
    putQuestionListApi(editingQuestion.value).then((res) => {
      if (res.value) {
        const index = questions.value.findIndex((q) => q.id === editingQuestion.value.id)
        if (index !== -1) {
          questions.value[index] = {
            ...questions.value[index],
            question: questionForm.question
          }
        }
      }
    })
  } else {
    // 新增问题
    addQuestionListApi({
      question: questionForm.question
    }).then((res) => {
      if (res.value) {
        questions.value.push({
          id: nextQuestionId.value,
          question: questionForm.question
        })
      }
    })
  }
  closeQuestionForm()
}

function deleteQuestion(questionId) {
  if (confirm('确定要删除这个问题吗？删除后相关答案也会被删除。')) {
    questions.value = questions.value.filter((q) => q.id !== questionId)
    answers.value = answers.value.filter((a) => a.question_id !== questionId)
    expandedQuestions.value.delete(questionId)
    delQuestionApi([questionId]).then((res) => {})
  }
}

// 答案相关方法
function openAnswerForm(questionId) {
  resetAnswerForm()
  answerForm.question_id = questionId
  showAnswerForm.value = true
}

function closeAnswerForm() {
  showAnswerForm.value = false
  editingAnswer.value = null
  resetAnswerForm()
}

function resetAnswerForm() {
  answerForm.question_id = null
  answerForm.answer = ''
  answerForm.next_question = ''
}

function editAnswer(answer) {
  editingAnswer.value = answer
  answerForm.question_id = answer.question_id
  answerForm.answer = answer.answer
  answerForm.next_question = answer.next_question || ''
  showAnswerForm.value = true
}

function saveAnswer() {
  if (editingAnswer.value) {
    // 更新答案
    editingAnswer.value.answer = answerForm.answer
    editingAnswer.value.next_question = answerForm.next_question || null
    putAnswerListApi(editingAnswer.value).then((res) => {
      if (res.value) {
        const index = answers.value.findIndex((a) => a.id === editingAnswer.value.id)
        if (index !== -1) {
          answers.value[index] = {
            ...answers.value[index],
            answer: answerForm.answer,
            next_question: answerForm.next_question || null
          }
        }
      }
    })
  } else {
    // 新增答案
    const newAnswers = {
      question_id: answerForm.question_id,
      answer: answerForm.answer,
      next_question: answerForm.next_question || null
    }
    addAnswerListApi(newAnswers).then((res) => {
      if (res.value) {
        answers.value.push({
          id: nextAnswerId.value,
          question_id: answerForm.question_id,
          answer: answerForm.answer,
          next_question: answerForm.next_question || null
        })
      }
    })
  }
  closeAnswerForm()
}

function deleteAnswer(answerId) {
  if (confirm('确定要删除这个答案吗？')) {
    delAnswerListApi([answerId]).then((res) => {
      if (res.value) {
        answers.value = answers.value.filter((a) => a.id !== answerId)
      }
    })
  }
}

// 展开/收起答案
function toggleAnswers(questionId) {
  if (expandedQuestions.value.has(questionId)) {
    expandedQuestions.value.delete(questionId)
  } else {
    expandedQuestions.value.add(questionId)
  }
}
</script>
