package helpers

import (
	"encoding/json"
	"io/ioutil"
	"net"
	"net/http"
)

func GetPublicIPAddress() (net.IP, error) {

	resp, err := http.Get("https://ipinfo.io/json")
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	resp_body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var Response interface{}
	json.Unmarshal(resp_body, &Response)

	ip := net.ParseIP(Response.(map[string]interface{})["ip"].(string))
	return ip, nil

}
