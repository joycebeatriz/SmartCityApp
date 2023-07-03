const axios = require('axios');
const { OrionClient } = require('fiware-orion-client');

const orionUrl = 'http://localhost:1026/';
const subscriptionUrl = `${orionUrl}v2/subscriptions`;

// Função para obter a lista de assinaturas no Orion Context Broker
async function getSubscriptions() {
  try {
    const response = await axios.get(subscriptionUrl);
    const subscriptions = response.data;
    return subscriptions;
  } catch (error) {
    throw new Error(`Failed to get subscriptions: ${error.message}`);
  }
}

// Criar uma instância do OrionClient
const orionClient = new OrionClient(orionUrl);

// Obter a lista de assinaturas
getSubscriptions()
  .then((subscriptions) => {
    console.log('Lista de assinaturas:', subscriptions);

    // Verificar se as assinaturas para as entidades 'ambulance' e 'hospital' existem
    const ambulanceSubscription = subscriptions.find(subscription => subscription.subject.entities[0].id === 'ambulance');
    const hospitalSubscription = subscriptions.find(subscription => subscription.subject.entities[0].id === 'hospital');

    // Verificar se as assinaturas existem e realizar as ações correspondentes
    if (ambulanceSubscription) {
      orionClient.subscribeEntity('ambulance', (entity) => {
        // Atualize o widget da ambulância com os dados recebidos
        const ambulanceWidget = MashupPlatform.widget.getWidget('ambulance-widget');
        ambulanceWidget.set('property', entity.property);
      });
    } else {
      console.log('Assinatura para entidade "ambulance" não encontrada');
    }

    if (hospitalSubscription) {
      orionClient.subscribeEntity('hospital', (entity) => {
        // Atualize o widget do hospital com os dados recebidos
        const hospitalWidget = MashupPlatform.widget.getWidget('hospital-widget');
        hospitalWidget.set('property', entity.property);
      });
    } else {
      console.log('Assinatura para entidade "hospital" não encontrada');
    }
  })
  .catch((error) => {
    console.error('Erro ao obter assinaturas:', error);
  });
