package main

import (
	"ddnsc/config"
	"ddnsc/providers"
	"time"
)

/**
* Define the interface for the Provider to later use
* in seperate providers to implement
 */
type Provider interface {
	Worker(cfg config.Provider)
}

/**
* Define list of available providers into the following
* factory var to utilize later in dynamic provider
* loading.
 */
var Factory map[string]Provider = map[string]Provider{
	"cloudflare": &providers.Cloudflare{},
}

func main() {

	/**
	* We have to load the configuration file from the disk to
	* grab predefine configuration data to the utility.
	 */
	config := config.NewConfig()

	for {

		for name, cfg := range config.Providers {
			var provider Provider = Factory[name]
			provider.Worker(cfg)
		}

		time.Sleep(time.Duration(config.Global.Interval) * time.Second)
	}

}
