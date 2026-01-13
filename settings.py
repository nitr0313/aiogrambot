import logging
from decouple import config


admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

token = config('TELEBOT_TOKEN')
