import config


app = config.conn_app
app.add_api("spec.yaml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
