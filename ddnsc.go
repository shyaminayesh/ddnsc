package main

import (
	"ddnsc/providers"
	"time"
)

/**
* Define the interface for the Provider to later use
* in seperate providers to implement
 */
type Provider interface {
	Worker(configuration map[string]interface{})
}

/**
* Define list of available providers into the following
* factory var to utilize later in dynamic provider
* loading.
 */
var Factory map[string]Provider = map[string]Provider{
	"test": &providers.Test{},
}

func main() {

	/**
	* We have to load the configuration file from the disk to
	* grab predefine configuration data to the utility.
	 */
	config := NewConfig()

	for {

		for name, configuration := range config.Provider {
			configuration := configuration.(map[string]interface{})
			var provider Provider = Factory[name]
			provider.Worker(configuration)
		}

		time.Sleep(time.Duration(config.Global.Interval) * time.Second)
	}

}
