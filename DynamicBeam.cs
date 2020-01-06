using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DynamicBeam : MonoBehaviour

{
    public GameObject mController; 　//コントローラオブジェクト
    private LineRenderer mBeamLine;　//光線

    void Start()
    {
        mBeamLine = GetComponent<LineRenderer>();   //光線を取得
        mBeamLine.startColor = Color.green;         //光線のスタートカラー
        mBeamLine.endColor = Color.red;
    }

    void Update()
    {
        //ビームをコントローラの位置と方向に合わせる
        transform.position = mController.transform.position;
        transform.rotation = mController.transform.rotation;

        //コントローラから前方へ出力された仮想光線がオブジェクトに当たっている場合に実行
        RaycastHit hit;
        if (Physics.Raycast(transform.position, transform.forward, out hit))
        {
            mBeamLine.useWorldSpace = true;
            mBeamLine.SetPosition(0, transform.position);　//光線の開始座標をコントローラに設定
            mBeamLine.SetPosition(1, hit.point);            //光線の終端座標をヒットポイントに設定
        }
        else
        {
            mBeamLine.useWorldSpace = false;
            mBeamLine.SetPosition(0, transform.position);
            mBeamLine.SetPosition(1, Vector3.forward * 5);  // 光線の終端座標を5m前方に設定
        }

    }
}
