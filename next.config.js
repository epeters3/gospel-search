module.exports = {
  serverRuntimeConfig: {
    // Will only be available on the server side
    ES_HOST: "http://localhost:9200", // Host URL of the ElasticSearch instance
    NLP_HOST: "http://localhost:5000" // Host URL of the Natural Language Processing reranking server.
  }
};
