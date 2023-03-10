/* eslint-disable no-unused-vars */
const Service = require('./Service');

/**
* Cadastra os dados de um novo pedido na plataforma
*
* requestData RequestData Dado do pedido a ser cadastrado
* returns Request
* */
const createRequest = ({ requestData }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        requestData,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Obtem os dados de um pedido existente por ID na plataforma
*
* requestId String ID do pedido
* returns Request
* */
const getRequest = ({ requestId }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        requestId,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Atualiza os dados de um pedido existente por ID na plataforma
*
* requestId String ID do pedido
* requestData RequestData Dado do pedido a ser atualizado
* returns Request
* */
const setRequest = ({ requestId, requestData }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        requestId,
        requestData,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);

module.exports = {
  createRequest,
  getRequest,
  setRequest,
};
