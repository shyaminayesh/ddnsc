package providers

import (
	"fmt"
	"net/http"
)

type Cloudflare struct {
	Client *http.Client
}

func (provider *Cloudflare) Worker(conf map[string]interface{}) {
	fmt.Println("Cloudflare::worker")
}
