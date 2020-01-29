using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SmallCube : MonoBehaviour
{

    // Update is called once per frame
    void Update()
    {
        
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "teritory")
        {
            transform.parent.gameObject.GetComponent<TetrisCubeScript>().EnterTetrisArea();
        }
    }

    void OnTriggerExit(Collider other)
    {
        if (other.gameObject.tag == "teritory")
        {
            transform.parent.gameObject.GetComponent<TetrisCubeScript>().ExitTetrisArea();
        }
    }
}
