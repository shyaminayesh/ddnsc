package main

import (
	"ddnsc/factories"
	"net/http"
	"reflect"
	"time"
)

func main() {

	/**
	* We have to load the configuration file from the disk to
	* grab predefine configuration data to the utility.
	 */
	config := Config()

	// ip := &net.IP{}
	for {

		for name, conf := range config.GetStringMap("provider") {
			Provider := factories.Providers[name]

			/**
			* Configure struct attribute for future use in the
			* provider methods. We can use common set of interfaces
			* if needed.
			 */
			reflect.ValueOf(Provider).Elem().FieldByName("Client").Set(reflect.ValueOf(&http.Client{}))

			/**
			* Invoke the worker method of the provider plugin
			* to do the actual work.
			 */
			reflect.ValueOf(Provider).MethodByName("Worker").Call([]reflect.Value{
				reflect.ValueOf(conf),
			})

		}

		time.Sleep(time.Duration(config.GetInt("global.interval")) * time.Second)
	}

}
