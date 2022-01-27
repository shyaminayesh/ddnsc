package factories

import "ddnsc/providers"

var Providers map[string]interface{} = map[string]interface{}{
	"cloudflare": &providers.Cloudflare{},
}
