/**
 * The ServicosController file is a very simple one, which does not need to be changed manually,
 * unless there's a case where business logic routes the request to an entity which is not
 * the service.
 * The heavy lifting of the Controller item is done in Request.js - that is where request
 * parameters are extracted and sent to the service, and where response is handled.
 */

const Controller = require('./Controller');
const service = require('../services/ServicosService');
const createService = async (request, response) => {
  await Controller.handleRequest(request, response, service.createService);
};

const getService = async (request, response) => {
  await Controller.handleRequest(request, response, service.getService);
};

const removeService = async (request, response) => {
  await Controller.handleRequest(request, response, service.removeService);
};

const setService = async (request, response) => {
  await Controller.handleRequest(request, response, service.setService);
};


module.exports = {
  createService,
  getService,
  removeService,
  setService,
};
