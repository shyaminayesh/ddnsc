package config

import (
	"log"
	"os"

	"github.com/pelletier/go-toml"
)

type (
	Provider struct {
		Token string
	}

	Config struct {
		Global struct {
			Interval uint64
		}

		Providers map[string]Provider `toml:"provider"`
	}
)

func NewConfig() Config {

	/**
	* Check for the configuration file in the default
	* locations to load into the Configuration struct
	*    Order:
	*      - ./ddnsc.conf
	*      - /etc/ddnsc/ddnsc.conf
	 */
	var file *os.File

	if _, err := os.Stat("./ddnsc.conf"); err == nil {
		file, err = os.Open("./ddnsc.conf")
		if err != nil {
			log.Fatal(err)
		}
	}

	if _, err := os.Stat("/etc/ddnsc/ddnsc.conf"); err == nil {
		file, err = os.Open("/etc/ddnsc/ddnsc.conf")
		if err != nil {
			log.Fatal(err)
		}
	}

	/**
	* Decode TOML file into the Configuration struct and then
	* return the Configuration struct to work with.
	 */
	config := Config{}
	err := toml.NewDecoder(file).Decode(&config)
	if err != nil {
		log.Fatal(err)
	}

	return config

}
