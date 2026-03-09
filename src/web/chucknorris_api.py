import requests
import json


class Chucknorris_jokes:

    _base_url = "https://api.chucknorris.io/jokes"
    _timeout = 2
    _common_headers = {"Content-Type":"application/json", "Accept":"application/json"}

    def __init__(self):
        self.__base_url = "https://api.chucknorris.io/jokes"
        self.__timeout = 2
        self.__common_headers = {"Content-Type":"application/json", "Accept":"application/json"}
    
    @classmethod
    def get_categories(cls) -> list:
        response = requests.get(url=f"{cls._base_url}/categories", 
                                timeout=cls._timeout,
                                headers=cls._common_headers)
        
        return json.dumps(response.json(), indent=3)

    @staticmethod
    def get_categories_static() -> list:
        response = requests.get(url=f"{Chucknorris_jokes._base_url}/categories", 
                                timeout=Chucknorris_jokes._timeout,
                                headers=Chucknorris_jokes._common_headers)
        
        return json.dumps(response.json(), indent=3)

    def get_categories_instanced(self) -> list:
        response = requests.get(url=f"{self.__base_url}/categories", 
                                timeout=self.__timeout,
                                headers=self.__common_headers)
        
        return json.dumps(response.json(), indent=3)
    
    def get_category_by_name(self, name: str = None) -> str:
        if name is None or isinstance(name, str):
            raise ValueError("Must indicate a name as string")
        
        parameters = dict(("category", name))
        response = requests.get(url=f"{self.__base_url}/random",
                                params=parameters,
                                timeout=self.__timeout,
                                headers=self.__common_headers)
        
        return response.json()
    
def main():

    print(f"Class method (decorator: @classmethod) response: \n {Chucknorris_jokes.get_categories()}")
    print(f"Instanced method: \n{Chucknorris_jokes().get_categories_instanced()}")
    print(f"Static method (decorator: @staticmethod) response: \n{Chucknorris_jokes.get_categories_static()}")

if __name__ == "__main__":
    main()