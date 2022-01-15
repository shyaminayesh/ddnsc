package main

import (
	"log"

	"github.com/spf13/viper"
)

func Config() *viper.Viper {

	config := viper.New()
	config.SetConfigName("ddnsc.conf")
	config.SetConfigType("toml")
	config.AddConfigPath(".")
	config.AddConfigPath("/etc/ddnsc")

	/**
	* Read configuration file from the disk and report any
	* errors to the logs happen during the operation.
	 */
	err := config.ReadInConfig()
	if err != nil {
		log.Println(err)
		log.Fatal("Failed to read main configuration file.")
	}

	// return
	return config

}
