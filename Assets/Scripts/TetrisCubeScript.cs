using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TetrisCubeScript : MonoBehaviour {


    public bool IsEnterTetrisArea = false;
    public bool IsCubeCollision = false;

    // Use this for initialization
    void Start () {
        transform.GetComponent<Renderer>().material.color = Color.cyan;
    }
	
	// Update is called once per frame
	void Update () {
		
	}

    public void EnterTetrisArea()
    {
        IsEnterTetrisArea = true;
        transform.GetComponent<Renderer>().material.color = Color.red;
    }

    public void ExitTetrisArea()
    {
        IsEnterTetrisArea = false;
        transform.GetComponent<Renderer>().material.color = Color.cyan;
    }

    void OnTriggerEnter(Collider other)
    {
        Debug.Log("aaaaaaaaaa");
        if (other.gameObject.tag == "tetris")
        {
            Debug.Log("yyyyyyyyyyy");
            IsCubeCollision = true;
        }
    }

    void OnTriggerExit(Collider other)
    {
        Debug.Log("bbbbbbbbb");
        if (other.gameObject.tag == "tetris")
        {
            Debug.Log("zzzzzzzzzzzz");
            IsCubeCollision = false;
        }
    }

    /*
void OnTriggerStay(Collider other)
{
   // transform.GetComponent<Renderer>().material.color = Color.red;
}
**/

    public void SetColor()
    {
        transform.GetComponent<Renderer>().material.color = Color.black;
    }

}
