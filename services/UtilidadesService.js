/* eslint-disable no-unused-vars */
const Service = require('./Service');

/**
* Obtem os IDs de todos os servicos existentes na plataforma
*
* returns List
* */
const getAllServiceIds = () => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
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
* Obtem os dados de todos os pedidos de servicos feitos para um usuario existente por ID
*
* userId String ID do usuario prestador
* returns List
* */
const getRequestsByUserId = ({ userId }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        userId,
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
  getAllServiceIds,
  getRequestsByUserId,
};
