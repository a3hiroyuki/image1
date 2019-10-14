using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using HoloLab.AzureKinect.NativeMethod;
using HoloLab.AzureKinect;
using System;

public class Sample : MonoBehaviour

{

    private KinectSensor mKs;
    private Capture mCapture;

    // Start is called before the first frame update
    void Start()
    {

        mKs = new KinectSensor();

        //カメラオープン
        mKs.Open();

        //IntPtr buffer = new IntPtr();
        //k4a_result_t result = K4A.k4a_device_open(1, out buffer);

        Debug.Log(mKs.GetSerialNumber());


        //カメラスタート
        DeviceConfiguration config = new DeviceConfiguration();
        config.CameraFps = Fps._30;
        config.ColorFormat = ImageFormat.ColorMJPG;
        config.ColorResolution = ColorResolution._2160P;
        config.DepthMode = DepthMode.NarrowFOV_Unbinned;
        mKs.StartCamera(config);


        mCapture = mKs.GetNextCapture();

    }

    // Update is called once per frame
    void Update()
    {
        Image image = mCapture.GetColorImage();
    }

    private void OnDestroy()
    {
        mKs.Close();
        mCapture.Close();
    }
}
