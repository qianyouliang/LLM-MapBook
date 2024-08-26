const state = {
    eventList: [],
}

const getters = {}

const mutations = {
    SET_EVENT_LIST: (state, eventList) => {
        state.eventList = eventList
    }
}
const actions = {

}

export default {
    nameSpaced: true,
    state,
    getters,
    mutations,
    actions,
};