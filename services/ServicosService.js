/* eslint-disable no-unused-vars */
const Service = require('./Service');

/**
* Cadastra os dados de um novo servico na plataforma
*
* serviceData ServiceData Dado do servico a ser cadastrado
* returns Service
* */
const createService = ({ serviceData }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        serviceData,
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
* Obtem os dados de um servico existente por ID na plataforma
*
* serviceId String ID do servico
* returns Service
* */
const getService = ({ serviceId }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        serviceId,
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
* Remove os dados de um servico existente por ID na plataforma
*
* serviceId String ID do usuario prestador
* no response value expected for this operation
* */
const removeService = ({ serviceId }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        serviceId,
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
* Atualiza os dados de um servico existente por ID na plataforma
*
* serviceId String ID do servico
* serviceData ServiceData Dado do servico a ser atualizado
* returns Service
* */
const setService = ({ serviceId, serviceData }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        serviceId,
        serviceData,
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
  createService,
  getService,
  removeService,
  setService,
};
