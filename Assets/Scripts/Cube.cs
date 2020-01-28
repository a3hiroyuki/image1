using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Cube : MonoBehaviour {

    private GameObject dlight;
    private MeshRenderer rendererx;
    public bool IsCollision = false;

	// Use this for initialization
	void Start () {
        //dlight = GameObject.Find("Directional Light");
        //rendererx = this.gameObject.GetComponent<MeshRenderer>();
        transform.GetComponent<Renderer>().material.color = Color.cyan;
    }
	
	// Update is called once per frame
	void Update () {
		
	}

    public void ChangeColor()
    {
        transform.GetComponent<Renderer>().material.color = Color.green;
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "teritory")
        {
            IsCollision = true;
            transform.GetComponent<Renderer>().material.color = Color.red;
        } 
    }

    /*
    void OnTriggerStay(Collider other)
    {
       // transform.GetComponent<Renderer>().material.color = Color.red;
    }
    **/

    void OnTriggerExit(Collider other)
    {
        if (other.gameObject.tag == "teritory")
        {
            IsCollision = false;
            transform.GetComponent<Renderer>().material.color = Color.cyan;
        }
    }

    public void SetColor()
    {
        transform.GetComponent<Renderer>().material.color = Color.magenta;
    }

    public void SetColor2()
    {
        transform.GetComponent<Renderer>().material.color = Color.black;
    }
}
