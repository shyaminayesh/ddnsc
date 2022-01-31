package providers

import (
	"bytes"
	"ddnsc/config"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
)

type Cloudflare struct{}

/**
* Validate provided configuration details in the
* configuration file to check if all the compulsory
* information is present
 */
func (provider Cloudflare) Validate(cfg config.Provider) error {
	return nil
}

/**
* Get Cloudflare DNS record identifier for the
* specified host in the configuration using API.
 */
func (provider Cloudflare) GetRecordIdentifier(cfg config.Provider) (string, error) {

	request, err := http.NewRequest(http.MethodGet, fmt.Sprintf("https://api.cloudflare.com/client/v4/zones/%s/dns_records?name=%s", cfg.Zone, cfg.Host), nil)
	if err != nil {
		return "", err
	}

	// Request headers
	request.Header = http.Header{
		"Content-type":  []string{"application/json"},
		"Authorization": []string{fmt.Sprintf("Bearer %s", cfg.Token)},
		"X-Auth-Key":    []string{cfg.Key},
		"X-Auth-Email":  []string{cfg.Email},
	}

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		return "", nil
	}

	body_bytes, err := io.ReadAll(response.Body)
	if err != nil {
		return "", err
	}
	defer response.Body.Close()

	var Response interface{}
	if err = json.Unmarshal(body_bytes, &Response); err != nil {
		return "", err
	}

	return Response.(map[string]interface{})["result"].([]interface{})[0].(map[string]interface{})["id"].(string), nil
}

/**
* Update the DNS record information with the new
* IP address.
 */
func (provider Cloudflare) Worker(cfg config.Provider) error {

	// Validate Configuration
	if err := provider.Validate(cfg); err != nil {
		return err
	}

	// Get Record Identifier
	identifier, err := provider.GetRecordIdentifier(cfg)
	if err != nil {
		return err
	}

	payload, err := json.Marshal(map[string]interface{}{
		"type":    "A",
		"name":    cfg.Host,
		"content": "127.0.0.2",
		"ttl":     cfg.TTL,
		"proxied": false,
	})
	if err != nil {
		return err
	}

	request, err := http.NewRequest(http.MethodPut, fmt.Sprintf("https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s", cfg.Zone, identifier), bytes.NewBuffer(payload))
	if err != nil {
		return err
	}

	// Request headers
	request.Header = http.Header{
		"Content-type":  []string{"application/json"},
		"Authorization": []string{fmt.Sprintf("Bearer %s", cfg.Token)},
		"X-Auth-Key":    []string{cfg.Key},
		"X-Auth-Email":  []string{cfg.Email},
	}

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		return err
	}

	response_body_bytes, err := io.ReadAll(response.Body)
	if err != nil {
		return err
	}
	defer response.Body.Close()

	var Response interface{}
	if err = json.Unmarshal(response_body_bytes, &Response); err != nil {
		return err
	}

	/**
	* Check if the response from the API return success status
	* as true and return error status back.
	 */
	if Response.(map[string]interface{})["success"].(bool) {
		return nil
	} else {
		return errors.New("error updating Cloudflare DNS record")
	}
}
