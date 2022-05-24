def read_config(filename: str) -> dict:
    teams = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("TEAM "):
                args = line[5:].split(":")
                team_name = args[0]
                if team_name in teams:
                    teams[team_name].update({
                        "color": args[1],
                        "details": args[2]
                    })
                else:
                    teams[team_name] = {
                        "color": args[1],
                        "details": args[2],
                        "models": []
                    }
                
            elif line.startswith("CAR "):
                args = line[4:].split(":")
                if len(args) < 2: continue # TODO print error instead

                team_name = args[0]
                h5_file_name = args[1]
                model_dict = {"model_file": h5_file_name}

                if len(args) > 2:
                    model_name = args[2]
                    model_dict["name"] = model_name
                
                
                if team_name not in teams:
                    teams[team_name] = {"models": [model_dict]}
                else:
                    teams[team_name]["models"].append(model_dict)


            else:
                # TODO Add other config stuff if necessary
                continue




    return {"TEAMS": teams}


if __name__ == "__main__":
    from pprint import pprint
    pprint(read_config(".conf.example"))
