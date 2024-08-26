import { fileUpload } from '@/api/index.js'
const state = {
    username: "",
    modelType: "deepseek",
    apiKey: "",
    geocodeType: "free",
    baiduKey: "",
    eventList: [],
    isRAG: false,
}

const getters = {}

const mutations = {
    // 设置用户名
    SET_USER_NAME(state, username) {
        state.username = username
    },
    // 设置模型类型
    SET_MODEL_TYPE(state, modelType) {
        state.modelType = modelType
    },
    // 设置API_KEY
    SET_API_KEY(state, apiKey) {
        state.apiKey = apiKey
    },
    // 设置地理编码类型
    SET_GEOCODE_TYPE(state, geocodeType) {
        state.geocodeType = geocodeType
    },
    // 设置百度地图APIkey
    SET_BAIDU_MAP_API(state, apiKey) {
        state.baiduKey = apiKey
    },
    // 设置聊天配置
    SET_CHAT_CONFIG(state, config) {
        state.useSmartMap = config.useSmartMap;
        state.useRAG = config.useRAG;
    },
    SET_IS_RAG(state, isRAG) {
        state.isRAG = isRAG;
    }
}
const actions = {
    async uploadFile(file) {
        let formData = new FormData();
        formData.append('uploaded_file', file);
        formData.append('model_type', this.modelType);
        formData.append('api_key', this.apiKey);
        formData.append('geocode_type', this.geocodeType);
        formData.append('baidu_key', this.baiduKey);
        formData.append('username', this.username);
        formData.append('use_rag', this.useRAG);
        formData.append('is_ragged', this.isRAG);

        let res = await fileUpload(formData);
        console.log(res.data, "这是文件上传的反馈信息");

    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
};