const state = {
    username: "",
    modelType: "deepseek",
    apiKey: "",
    geocodeType: "free",
    baiduKey: "",
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
}
const actions = {

}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
};