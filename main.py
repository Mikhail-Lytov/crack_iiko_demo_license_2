import src.create_new_document as create_new_document
import yaml
import os
import logging

logger = logging.getLogger()

def log():
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('crack_iikoRMS_demo_license.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

def load_yaml(filepath):
    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            logger.info("the config has been read")
            return data
    except FileNotFoundError:
        logger.error(f"Файл {filepath} не найден.")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Ошибка при чтении YAML файла: {e}")
        return None


if __name__ == '__main__':

    log()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "config.yml")

    config = load_yaml(yaml_path)

    create_new_document.create_new_document(config["item_test"], config["url_iiko"], config["url_login"], config["url_password"])