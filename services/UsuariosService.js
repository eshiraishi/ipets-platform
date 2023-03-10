/* eslint-disable no-unused-vars */
const Service = require('./Service');

/**
* Cadastra os dados de um novo usuario na plataforma
*
* userData UserData Dados do usuario a ser cadastrado
* returns User
* */
const createUser = ({ userData }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        userData,
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
* Obtem os dados de um usuario existente por ID na plataforma
*
* userId String ID do usuario
* returns User
* */
const getUser = ({ userId }) => new Promise(
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
/**
* Remove os dados de um usuario existente por ID na plataforma
*
* userId String ID do usuario
* no response value expected for this operation
* */
const removeUser = ({ userId }) => new Promise(
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
/**
* Atualiza os dados de usuario existente por ID na plataforma
*
* userId String ID do usuario
* userData UserData Dados do usuario a ser atualizado
* returns User
* */
const setUser = ({ userId, userData }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        userId,
        userData,
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
  createUser,
  getUser,
  removeUser,
  setUser,
};
