import {fetchFilterList} from "../../api/index"

const fromDate = new Date()
fromDate.setDate(new Date().getDate() - 3)
const toDate = new Date()

export default {
    namespaced: true,
    state: {
        filter: [],
        selectOptName: "Select..",
        searchText: "",
        from: fromDate,
        to: toDate,
        mdValues: [],
        Limit: 50,
        isFetched: false
    },
    getters: {
        filterData(state) {
            return state.filter
        },
        optNameData(state) {
            return state.selectOptName
        },
        fromData(state) {
          return state.from
        },
        toData(state) {
          return state.to
        },
        mdValues(state) {
          return state.mdValues
        },
        LimitData(state) {
          return state.Limit
        },
        isFetch(state) {
          return state.isFetched
        }
    },
    mutations: {
        setFilter(state, data) {
          state.filter = data;
          state.isFetched = false
        },
        setLimit(state, data) {
          state.Limit = data
        },
        setMdValues(state, data) {
          state.mdValues = data
        },
        setOptName(state, optName) {
            if(optName === "주문번호"){
              return state.selectOptName = 'order_number'
            } 
            if(optName === "주문상세번호"){
                return state.selectOptName = 'detail_number'
            }
            if(optName === "주문자명"){
                return state.selectOptName = 'user_name'  
            }
            if(optName === "핸드폰번호"){
                return state.selectOptName = 'phone_number'
            }
            if(optName === "셀러명"){
                return state.selectOptName = 'seller_name'
            }
            if(optName === "상품명"){
                return state.selectOptName = 'product_name'
            }
               state.selectOptName = optName
        },
        setText(state, text) {
            return state.searchText = text
        },  
        setDate(state, data) {
          if (data.item.name === "전체") {
              state.from = "";
              state.to = "";
            }
            if (data.item.name === "오늘") {
              const today = new Date();
              state.from = today;
              state.to = today;
            }
            if (data.item.name === "3일") {
              const today = new Date();
              today.setDate(today.getDate() - 3);
              state.from = today;
              state.to = new Date();
            }
            if (data.item.name === "1주일") {
              const today = new Date();
              today.setDate(today.getDate() - 7);
              state.from = today;
              state.to = new Date();
            }
            if (data.item.name === "1개월") {
              const today = new Date();
              today.setMonth(today.getMonth() - 1);
              state.from = today;
              state.to = new Date();
            }
            if (data.item.name === "3개월") {
              const today = new Date();
              today.setMonth(today.getMonth() - 3);
              state.from = today;
              state.to = new Date();
            }
      },
    },
    actions: {
      fetchFilter(context) {
        context.state.isFetched = true

        const getDate = (date) => {
          if(`${date}`.length === 0) {
            return date
          }
          let year = date.getFullYear();
          let month = date.getMonth() + 1;
          let day = date.getDate();

          if(`${month}`.length < 2 && `${day}`.length < 2){
            return `${year}-0${month}-0${day}`
          }
          if(`${month}`.length === 2 && `${day}`.length === 2) {
            return `${year}-${month}-${day}`
          }
          if(`${month}`.length < 2) {
             return`${year}-0${month}-${day}`
          }
          if(`${day}`.length < 2){
           return `${year}-${month}-0${day}`
          }   
        }
        const getMd = (data) => {
          if(data.length === 0) {
            return [1,2,3,4,5,6,7];
          }
          return data
        }
        const data = {
            optName: context.state.selectOptName,
            inputData: context.state.searchText,
            startDate: getDate(context.state.from),
            endDate: getDate(context.state.to),
            mdData: getMd(context.state.mdValues),
            limit: context.state.Limit
          }
        fetchFilterList(data)
            .then(responese => {
              console.log("responese",responese)
                context.commit("setFilter", responese.data);
            })
            .catch(error => {
              console.log(error);
              context.state.isFetched = false;
            })
        },
        setFromDate(context, data) {
          context.state.from = data
        },
        setToDate(context, data) {
          context.state.to = data
        },
        setLimit(context, data) {
          context.state.Limit = data
        }
    },
}