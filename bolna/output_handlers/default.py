import base64
from dotenv import load_dotenv
from bolna.helpers.logger_config import configure_logger

logger = configure_logger(__name__)
load_dotenv()


class DefaultOutputHandler:
    def __init__(self, websocket=None, mark_set=None, log_dir_name=None):
        self.websocket = websocket
        self.is_interruption_task_on = False

    # @TODO Figure out the best way to handle this
    async def handle_interruption(self):
        logger.info("#######   Sending interruption message ####################")
        response = {"data": None, "type": "clear"}
        await self.websocket.send_json(response)


    async def handle(self, packet):
        try:
            logger.info(f"Packet received:")
            data = None
            if packet["meta_info"]['type'] in ('audio', 'text'):
                if packet["meta_info"]['type'] == 'audio':
                    logger.info(f"Sending audio")
                    with open('audio1.wav', 'wb') as f:
                        f.write(packet['data'])
                    data = base64.b64encode(packet['data']).decode("utf-8")
                    #logger.info(f"data -> {data}")
                elif packet["meta_info"]['type'] == 'text':
                    logger.info(f"Sending text response {packet['data']}")
                    data = packet['data']

                response = {"data": data, "type": packet["meta_info"]['type']}
                await self.websocket.send_json(response)

            else:
                logger.error("Other modalities are not implemented yet")
        except Exception as e:
            logger.error(f"something went wrong in speaking {e}")
