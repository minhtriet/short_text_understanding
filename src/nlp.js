const server_url = "localhost:5000/api/v1/";

export const process = (query) => {
    fetch(server_url)
      .then(response => response.json());
}
