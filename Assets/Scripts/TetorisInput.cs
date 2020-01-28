using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TetorisInput : MonoBehaviour
{

    public bool Is_Left = false;
    public bool Is_Right = false;
    public bool Is_Up = false;
    public bool Is_Down = false;
    public bool Is_SideRotate = false;
    public bool Is_VerticalRotate = false;
    public bool Is_Drop  = false;

    public void PushLeftButton()
    {
        Is_Left = true;
    }
    public void PushRightButton()
    {
        Is_Right = true;
    }
    public void PushUpButton()
    {
        Is_Up = true;
    }
    public void PushDownButton()
    {
        Is_Down = true;
    }
    public void PushSideRotateButton()
    {
        Is_SideRotate = true;
    }
    public void PushVerticalRotateButton()
    {
        Is_VerticalRotate = true;
    }
    public void PushDropButton()
    {
        Is_Drop = true;
    }


    public void InitButton()
    {
        Is_Left = false;
        Is_Right = false;
        Is_Up = false;
        Is_Down = false;
        Is_SideRotate = false;
        Is_VerticalRotate = false;
        Is_Drop = false;
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
