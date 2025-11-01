<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-gray-800">
            {{ props.tabParams.title }}
            <ElButton @click="saveQATemplate" color="blue">✔保存</ElButton>
            <ElButton @click="fetchQuestionList" color="amber">⭕刷新</ElButton>
          </h1>
          <ElButton
            @click="openQuestionForm"
            color="blue"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            新增问题
          </ElButton>
        </div>

        <!-- 问题列表 -->
        <div class="space-y-4">
          <div
            v-for="(question, index) in questions"
            :key="question.id"
            class="border border-gray-200 rounded-lg p-4"
          >
            <div class="flex justify-between items-start mb-3">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">
                  问题 #{{ index + 1 }}: {{ question.question }}
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
            <div v-for="(question, index) in questions" :key="question.id" class="text-sm">
              <span class="font-medium text-blue-600"
                >问题 #{{ index + 1 }} {{ question.question }}</span
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
            <ElInput
              type="textarea"
              v-model="questionForm.question"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows="4"
              placeholder="请输入问题内容..."
              required
            />
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
            <ElInput
              type="textarea"
              v-model="answerForm.answer"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              rows="3"
              placeholder="请输入答案内容..."
              required
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">客户打的标签（可选）</label>
            <ElInput
              type="text"
              v-model="answerForm.customer_tag"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              placeholder="回答这问题之后给客户打的标签,默认为空"
            />
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-2">下一个问题（可选）</label>
            <ElSelect
              v-model="answerForm.next_question"
              class="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <ElOption value="">无跳转</ElOption>
              <ElOption
                v-for="q in questions"
                :key="q.id"
                :value="q.id"
                :label="q.question.substring(0, 50)"
              >
                问题 #{{ q.id }}: {{ q.question.substring(0, 50)
                }}{{ q.question.length > 50 ? '...' : '' }}
              </ElOption>
            </ElSelect>
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
import { ref, reactive, computed, onMounted, watchEffect, watch } from 'vue'
import {
  getQuestionListApi,
  delQuestionApi,
  addQuestionListApi,
  putQuestionListApi,
  getAnswerListApi,
  addAnswerListApi,
  putAnswerListApi,
  delAnswerListApi,
  getTemplateQuestionListApi,
} from '@/api/bot/qa/questiong'
import { ElButton, ElInput, ElOption, ElSelect, ElTabs, ElTabPane } from 'element-plus'

const props = defineProps({
  tabParams: {
    type: Object,
    default: () => ({}),
  },
})
const emit = defineEmits(['switch-tab'])

// 数据状态
const questions = ref([])

const answers = ref([])

// UI状态
const showQuestionForm = ref(false)
const showAnswerForm = ref(false)
const expandedQuestions = ref(new Set())
const editingQuestion = ref(null)
const editingAnswer = ref(null)

// 表单数据
const questionForm = reactive({
  question: '',
  template_id: props.tabParams.id,
})

const answerForm = reactive({
  question_id: null,
  answer: '',
  next_question: '',
  customer_tag: '',
})

const saveQATemplate = async () => {
  console.log(props.tabParams)
}

onMounted(() => {
  fetchQuestionList()
})

const fetchQuestionList = async () => {
  // const res = await getQuestionListApi({
  const res = await getTemplateQuestionListApi({
    template_id: props.tabParams.id || 0,
  })
  if (res.code === 200 && res.data) {
    questions.value = res.data
    const ansRes = await getAnswerListApi()
    if (ansRes.code === 200 && ansRes.data) {
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
    editingQuestion.value.template_id = props.tabParams.id
    putQuestionListApi(editingQuestion.value).then((res) => {
      if (res.value) {
        const index = questions.value.findIndex((q) => q.id === editingQuestion.value.id)
        if (index !== -1) {
          questions.value[index] = {
            ...questions.value[index],
            question: questionForm.question,
          }
        }
      }
    })
  } else {
    // 新增问题
    addQuestionListApi({
      question: questionForm.question,
      template_id: props.tabParams.id,
    }).then((res) => {
      if (res.value) {
        questions.value.push({
          id: nextQuestionId.value,
          question: questionForm.question,
        })
      }
    })
  }
  fetchQuestionList()
  closeQuestionForm()
}

function deleteQuestion(questionId) {
  if (confirm('确定要删除这个问题吗？删除后相关答案也会被删除。')) {
    questions.value = questions.value.filter((q) => q.id !== questionId)
    answers.value = answers.value.filter((a) => a.question_id !== questionId)
    expandedQuestions.value.delete(questionId)
    delQuestionApi([questionId]).then((res) => {
      fetchQuestionList()
    })
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
  answerForm.customer_tag = ''
}

function editAnswer(answer) {
  editingAnswer.value = answer
  answerForm.question_id = answer.question_id
  answerForm.answer = answer.answer
  answerForm.next_question = answer.next_question || ''
  answerForm.customer_tag = answer.customer_tag || ''
  showAnswerForm.value = true
}

function saveAnswer() {
  if (editingAnswer.value) {
    // 更新答案
    editingAnswer.value.answer = answerForm.answer
    editingAnswer.value.next_question = answerForm.next_question || null
    editingAnswer.value.customer_tag = answerForm.customer_tag || ''
    putAnswerListApi(editingAnswer.value).then((res) => {
      if (res.value) {
        const index = answers.value.findIndex((a) => a.id === editingAnswer.value.id)
        if (index !== -1) {
          answers.value[index] = {
            ...answers.value[index],
            answer: answerForm.answer,
            next_question: answerForm.next_question || null,
            customer_tag: answerForm.customer_tag || '',
          }
        }
      }
    })
  } else {
    // 新增答案
    const newAnswers = {
      question_id: answerForm.question_id,
      answer: answerForm.answer,
      next_question: answerForm.next_question || null,
      customer_tag: answerForm.customer_tag || '',
    }
    addAnswerListApi(newAnswers).then((res) => {
      if (res.value) {
        answers.value.push({
          id: nextAnswerId.value,
          question_id: answerForm.question_id,
          answer: answerForm.answer,
          next_question: answerForm.next_question || null,
          customer_tag: answerForm.customer_tag || '',
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
watch(
  () => props.tabParams.id,
  (newVal, oldVal) => {
    console.log('tabParams changed:', newVal)
    // fetchQuestionList()
  },
  { deep: true } // 👈 必须加 deep 才能监听对象内部变化
)
onMounted(async () => {
  console.log('===================', props)
})
</script>
