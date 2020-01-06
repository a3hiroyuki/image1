using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.MagicLeap;

public class ManuplateObject : MonoBehaviour
{
    private MLInputController mInputController; //コントローラオブジェクト
    private GameObject mSelectedObject;　　　　 //光線で補足したオブジェクト
    public GameObject mAttachPoint;             //光線が当たった座標を保持するオブジェクト
    bool isTrigger;                             //トリガ複数回起動を阻止フラグ

    void Start()
    {
        MLInput.Start();
        mInputController = MLInput.GetController(MLInput.Hand.Left);
    }

    private void UpdateTriggerInfo()
    {
        //トリガが押されていたら実行
        if (mInputController.TriggerValue > 0.8f)
        {
            if (isTrigger)  
            {
                RaycastHit hit;
                // コントローラから前方へ出力される仮想光線がオブジェクトに当たっているか判定
                if (Physics.Raycast(mInputController.Position, transform.forward, out hit))
                {
                    mSelectedObject = hit.transform.gameObject;                     //仮想光線が当たった場所のオブジェクト
                    mSelectedObject.GetComponent<Rigidbody>().useGravity = false;   //重力を解除
                    mAttachPoint.transform.position = hit.transform.position;       //仮想光線が当たった座標
                }
            }
            isTrigger = false;
        }
        //トリガが離されたら実行
        if (mInputController.TriggerValue < 0.2f)
        {
            isTrigger = true;
            //光線にオブジェクトが補足されたら実行
            if (mSelectedObject != null)
            {
                mSelectedObject.GetComponent<Rigidbody>().useGravity = true;　　　//重力を復帰
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        //ビームをコントローラの位置と方向に合わせる
        transform.position = mInputController.Position;
        transform.rotation = mInputController.Orientation;
        //光線にオブジェクトが補足されてるかどうか
        if (mSelectedObject != null)
        {
            mSelectedObject.transform.position = mAttachPoint.transform.position;　//仮想光線の座標をオブジェクトに設定
        }
        UpdateTriggerInfo();
    }

    private void OnDestroy()
    {
        MLInput.Stop();
    }
}
