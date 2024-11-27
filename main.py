import scheduler.scheduler as scheduler
import yaml
import os

def load_yaml(filepath):
    try:
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Файл {filepath} не найден.")
        return None
    except yaml.YAMLError as e:
        print(f"Ошибка при чтении YAML файла: {e}")
        return None


if __name__ == '__main__':

    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, "config.yml")

    config = load_yaml(yaml_path)

    scheduler.start_scheduler(config["item_test"], config["url_iiko"], config["url_login"], config["url_password"])