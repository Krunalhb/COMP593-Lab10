import requests
import image_lib
import os

POKE_API_URL = "https://pokeapi.co/api/v2/pokemon/"

def main():
    download_pokemon_artwork('ninetales', r'C:\temp')

    return
 
def get_pokemon_info(pokemon_name):
    """
    Gets information about a specified Pokémon from the PokéAPI.
    
    Args:
        pokemon (str or int): The name or Pokédex number of the Pokémon to fetch.
    
    Returns:
        dict: A dictionary containing all the Pokémon information fetched from the PokéAPI, if retrieved
        successfully. Returns None if the Pokémon information is not fetched successfully.
    """
    pokemon_name = str(pokemon_name).strip().lower()

    # Construct the API URL for the specified Pokémon
    url = POKE_API_URL + pokemon_name

    # Send Get request for pokemon info
    print(f'Getting information for {pokemon_name}...', end='')
    resp_msg = requests.get(url)

    # Check if the request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
       # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')         
        return
 

def get_pokemon_names(offset=0, limit=100000):
    
    query_str_params = {
        'offset' : offset,
        'limit' : limit
    }
    

    print('Getting list of Pokemon names...', end='')
    resp_msg = requests.get(POKE_API_URL, params=query_str_params)
    
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        pokemon_dict = resp_msg.json()
        pokemon_names_list = [p['name'] for p in pokemon_dict['results']]
        return pokemon_names_list
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return
    
def download_pokemon_artwork(pokemon_names, save_dir):
  
    # Get all info for the specified Pokemon
    pokemon_info = get_pokemon_info(pokemon_names)
    if pokemon_info is None:
        return
  
    # Extract the artwork URL from the info dictionary
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']

    # Download the artwork
    image_bytes = image_lib.download_image(artwork_url)
    if image_bytes is None:
        return
    
    # Determine the image file path
    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(save_dir, f'{pokemon_names}.{file_ext}')
    
    # Save the image file
    if image_lib.save_image_file(image_bytes, image_path):
        return image_path

    

if __name__ == '__main__':
    main()