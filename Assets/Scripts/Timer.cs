using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Timer : MonoBehaviour
{

    public GameObject HelloARController;

    private HelloARController2 mARControllerScript;
    private float seconds = 0;
    
    void Start()
    {
        mARControllerScript = (HelloARController2)HelloARController.GetComponent<HelloARController2>();
    }

    // Update is called once per frame
    void Update()
    {
        seconds += Time.deltaTime;
        if (seconds > 10.0f)
        {
            mARControllerScript.TimeOver();
            seconds = 0.0f;
        }
    }
}
