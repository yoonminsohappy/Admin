import axios from "axios"

export const config = 'http://3.35.156.251:5000/'

export const fetchFilterList = (data) => {
    if(data.optName === "Select.." && data.inputData === ""){
        return axios.get(`${config}order?offset=0&limit=${data.limit}&status_id=1&start_date=${data.startDate}&end_date=${data.endDate}&seller_properties=${data.mdData}`)
    }
    else {
        return axios.get(`${config}order?offset=0&limit=${data.limit}&status_id=1&${data.optName}=${data.inputData}&start_date=${data.startDate}&end_date=${data.endDate}&seller_properties=${data.mdData}`)
    }
}