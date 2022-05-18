def read_config(filename: str) -> dict:
    config = {
        "TEAMS": {}
    }
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line[0:4] == "CAR ":
                colon = line.find(":")
                if colon < 0: continue # TODO print error instead
                team_name = line[4:colon]
                h5_file_name = line[colon+1:]
                if team_name not in config["TEAMS"]:
                    config["TEAMS"][team_name] = [h5_file_name]
                else:
                    config["TEAMS"][team_name].append(h5_file_name)


            else:
                # TODO Add other config stuff if necessary
                continue
    return config


if __name__ == "__main__":
    print(read_config(".conf.example"))
