package providers

import "fmt"

type Test struct {
	Sample string
}

func (provider Test) Worker(config map[string]interface{}) {
	fmt.Println(config)
	fmt.Println("Test::worker")
}
