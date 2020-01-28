//-----------------------------------------------------------------------
// <copyright file="HelloARController.cs" company="Google">
//
// Copyright 2017 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// </copyright>
//-----------------------------------------------------------------------


using System.Collections.Generic;
using GoogleARCore;
using GoogleARCore.Examples.Common;
using UnityEngine;
using UnityEngine.EventSystems;

#if UNITY_EDITOR
// Set up touch input propagation while using Instant Preview in the editor.
using Input = GoogleARCore.InstantPreviewInput;
#endif

/// <summary>
/// Controls the HelloAR example.
/// </summary>
public class HelloARController2 : MonoBehaviour
{
    /// <summary>
    /// The first-person camera being used to render the passthrough camera image (i.e. AR
    /// background).
    /// </summary>
    public Camera FirstPersonCamera;

    /// <summary>
    /// A prefab to place when a raycast from a user touch hits a vertical plane.
    /// </summary>
    public GameObject GameObjectVerticalPlanePrefab;

    /// <summary>
    /// A prefab to place when a raycast from a user touch hits a horizontal plane.
    /// </summary>
    public GameObject GameObjectHorizontalPlanePrefab;

    /// <summary>
    /// A prefab to place when a raycast from a user touch hits a feature point.
    /// </summary>
    public GameObject GameObjectPointPrefab;

    /// <summary>
    /// The rotation in degrees need to apply to prefab when it is placed.
    /// </summary>
    private const float k_PrefabRotation = 180.0f;

    /// <summary>
    /// True if the app is in the process of quitting due to an ARCore connection error,
    /// otherwise false.
    /// </summary>
    private bool m_IsQuitting = false;


    //add
    public GameObject GameArea;
    public GameObject PlaneGenerator;
    public GameObject TetrisPrefab;
    private bool IsFirst = true;
    private General.Block[] blocks;
    private Anchor mAnchor;
    private Vector3 mTetrisDispPosi;
    private List<GameObject> mTetrisList;
    private Vector3 mTetrisDir;

    /// <summary>
    /// The Unity Awake() method.
    /// </summary>
    public void Awake()
    {
        // Enable ARCore to target 60fps camera capture frame rate on supported devices.
        // Note, Application.targetFrameRate is ignored when QualitySettings.vSyncCount != 0.
        Application.targetFrameRate = 60;
        blocks = General.generateBlockTemplate();
    }

    public void TimeOver()
    {
        CreateTetris();
    }

    public void Update()
    {
        if (mTetrisList != null && mTetrisList.Count > 0)
        {
            
            foreach (GameObject tetris in mTetrisList)
            {
                BlockBase2 currentScript = (BlockBase2)tetris.GetComponent(typeof(BlockBase2));
                if (currentScript.IsHolding())
                {
                    CheckInput(tetris);
                }
                if (currentScript.IsInTeritory2 && !currentScript.IsHolding())
                {
                    Debug.Log("xxxx");
                    Main script = (Main)GameArea.GetComponent(typeof(Main));
                    script.AddNextBlock2(tetris);
                    mTetrisList.Remove(tetris);
                }
            }
        }

        _UpdateApplicationLifecycle();

        // If the player has not touched the screen, we are done with this update.
        Touch touch;
        if (Input.touchCount < 1 || (touch = Input.GetTouch(0)).phase != TouchPhase.Began)
        {
            return;
        }

        // Should not handle input if the player is pointing on UI.
        if (EventSystem.current.IsPointerOverGameObject(touch.fingerId))
        {
            return;
        }

        // Raycast against the location the player touched to search for planes.
        TrackableHit hit;
        TrackableHitFlags raycastFilter = TrackableHitFlags.PlaneWithinPolygon |
            TrackableHitFlags.FeaturePointWithSurfaceNormal;

        if (Frame.Raycast(touch.position.x, touch.position.y, raycastFilter, out hit))
        {
            // Use hit pose and camera pose to check if hittest is from the
            // back of the plane, if it is, no need to create the anchor.
            if ((hit.Trackable is DetectedPlane) &&
                Vector3.Dot(FirstPersonCamera.transform.position - hit.Pose.position, hit.Pose.rotation * Vector3.up) < 0)
            {
                Debug.Log("Hit at back of the current DetectedPlane");
            }
            else
            {
                // Choose the prefab based on the Trackable that got hit.
                GameObject prefab;
                if (hit.Trackable is FeaturePoint)
                {
                    prefab = GameObjectPointPrefab;
                }
                else if (hit.Trackable is DetectedPlane)
                {
                    DetectedPlane detectedPlane = hit.Trackable as DetectedPlane;
                    if (detectedPlane.PlaneType == DetectedPlaneType.Vertical)
                    {
                        prefab = GameObjectVerticalPlanePrefab;
                    }
                    else
                    {
                        prefab = GameObjectHorizontalPlanePrefab;
                    }
                }
                else
                {
                    prefab = GameObjectHorizontalPlanePrefab;
                }

                if (IsFirst)
                {
                    IsFirst = false;
                    mAnchor = hit.Trackable.CreateAnchor(hit.Pose);
                    GameArea.SetActive(true);
                    GameArea.GetComponent<Main>().GameStart();
                    GameArea.transform.position = new Vector3(hit.Pose.position.x, hit.Pose.position.y, hit.Pose.position.z);
                    GameArea.transform.parent = mAnchor.transform;
                    Vector3 cameraDir = FirstPersonCamera.transform.position - GameArea.transform.position;
                    mTetrisDir = new Vector3(-cameraDir.x, 0, -cameraDir.z);
                    GameArea.transform.forward = mTetrisDir;
                    //PlaneGenerator.SetActive(false);
                }
                else
                {
                    if (mTetrisList == null)
                    {
                        mTetrisDispPosi = new Vector3(hit.Pose.position.x, hit.Pose.position.y + 0.3f, hit.Pose.position.z);
                        mTetrisList = new List<GameObject>();
                        CreateTetris();
                    }
                }
            }
        }
    }

    private void CreateTetris()
    {
        GameObject tetris = Instantiate(TetrisPrefab);
        BlockBase2 currentScript = (BlockBase2)tetris.GetComponent(typeof(BlockBase2));
        currentScript.block = blocks[1];
        currentScript.createCubes();
        currentScript.mRotateCenter = mTetrisDir;
        float rand = Random.Range(-0.3f, 0.3f);
        tetris.transform.position = new Vector3(mTetrisDispPosi.x + rand, mTetrisDispPosi.y, mTetrisDispPosi.z + rand);
        tetris.transform.forward = mTetrisDir;
        mTetrisList.Add(tetris);
    }

    private void CheckInput(GameObject tetris_block)
    {
        Vector3 posi = tetris_block.transform.localPosition;
        if (GetComponent<TetorisInput>().Is_Up)
        {
            tetris_block.transform.localPosition = new Vector3(posi.x, posi.y + 0.05f, posi.z);
        }
        if (GetComponent<TetorisInput>().Is_Down)
        {
            tetris_block.transform.localPosition = new Vector3(posi.x, posi.y - 0.05f, posi.z);
        }
        if (GetComponent<TetorisInput>().Is_SideRotate)
        {
            tetris_block.GetComponent<BlockBase2>().rotateRight();
        }
            
        if (GetComponent<TetorisInput>().Is_VerticalRotate)
        {
            tetris_block.GetComponent<BlockBase2>().rotateLeft();
        }
            
        GetComponent<TetorisInput>().InitButton();
    }

    /// <summary>
    /// Check and update the application lifecycle.
    /// </summary>
    private void _UpdateApplicationLifecycle()
    {
        // Exit the app when the 'back' button is pressed.
        if (Input.GetKey(KeyCode.Escape))
        {
            Application.Quit();
        }

        // Only allow the screen to sleep when not tracking.
        if (Session.Status != SessionStatus.Tracking)
        {
            Screen.sleepTimeout = SleepTimeout.SystemSetting;
        }
        else
        {
            Screen.sleepTimeout = SleepTimeout.NeverSleep;
        }

        if (m_IsQuitting)
        {
            return;
        }

        // Quit if ARCore was unable to connect and give Unity some time for the toast to
        // appear.
        if (Session.Status == SessionStatus.ErrorPermissionNotGranted)
        {
            _ShowAndroidToastMessage("Camera permission is needed to run this application.");
            m_IsQuitting = true;
            Invoke("_DoQuit", 0.5f);
        }
        else if (Session.Status.IsError())
        {
            _ShowAndroidToastMessage(
                "ARCore encountered a problem connecting.  Please start the app again.");
            m_IsQuitting = true;
            Invoke("_DoQuit", 0.5f);
        }
    }

    /// <summary>
    /// Actually quit the application.
    /// </summary>
    private void _DoQuit()
    {
        Application.Quit();
    }

    /// <summary>
    /// Show an Android toast message.
    /// </summary>
    /// <param name="message">Message string to show in the toast.</param>
    private void _ShowAndroidToastMessage(string message)
    {
        AndroidJavaClass unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
        AndroidJavaObject unityActivity =
            unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");

        if (unityActivity != null)
        {
            AndroidJavaClass toastClass = new AndroidJavaClass("android.widget.Toast");
            unityActivity.Call("runOnUiThread", new AndroidJavaRunnable(() =>
            {
                AndroidJavaObject toastObject =
                    toastClass.CallStatic<AndroidJavaObject>(
                        "makeText", unityActivity, message, 0);
                toastObject.Call("show");
            }));
        }
    }
}
