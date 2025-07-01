import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000/ws';

interface ToolActivity {
  action?: string;
  query?: string;
  url?: string;
  found_urls?: string[];
  error?: string;
  agent_thinking?: string;
  thinking_timestamp?: number;
}

interface ResearchResult {
  research_id: string;
  status: string;
  progress: number;
  message?: string;
  result?: any;
  slides_html?: string;
  error?: string;
  tool_activity?: ToolActivity;
}

function App() {
  const [query, setQuery] = useState('');
  const [modelId, setModelId] = useState('gpt-4o');
  const [maxSlides, setMaxSlides] = useState(6);
  const [isResearching, setIsResearching] = useState(false);
  const [currentResearch, setCurrentResearch] = useState<ResearchResult | null>(null);
  const [slidesHtml, setSlidesHtml] = useState<string | null>(null);
  const [toolActivities, setToolActivities] = useState<ToolActivity[]>([]);
  const [agentThinking, setAgentThinking] = useState<string[]>([]);
  const [showThinking, setShowThinking] = useState(true);
  const ws = useRef<WebSocket | null>(null);
  const thinkingScrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // WebSocket接続
    const connectWebSocket = () => {
      // 既存の接続がある場合は閉じる
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.close();
      }
      
      ws.current = new WebSocket(WS_URL);
      
      ws.current.onopen = () => {
        console.log('WebSocket connected');
      };
      
      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      };
      
      ws.current.onerror = (error) => {
        // 開発環境での接続エラーは無視
        if (process.env.NODE_ENV === 'development' && ws.current?.readyState === WebSocket.CLOSING) {
          return;
        }
        console.error('WebSocket error:', error);
        if (ws.current?.readyState !== WebSocket.CLOSING) {
          toast.error('WebSocket接続エラー');
        }
      };
      
      ws.current.onclose = (event) => {
        // 正常なクローズは無視
        if (event.wasClean) {
          console.log('WebSocket disconnected cleanly');
        } else {
          console.log('WebSocket disconnected unexpectedly');
          // 5秒後に再接続を試みる
          if (!isResearching) {
            setTimeout(connectWebSocket, 5000);
          }
        }
      };
    };
    
    connectWebSocket();
    
    return () => {
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.close();
      }
    };
  }, [isResearching]);

  const handleWebSocketMessage = (data: ResearchResult) => {
    setCurrentResearch(data);
    
    // ツールアクティビティの処理
    if (data.tool_activity) {
      // LLMの思考過程の場合
      if (data.tool_activity.agent_thinking) {
        setAgentThinking(prev => [...prev, data.tool_activity.agent_thinking!]);
        // 自動スクロール
        setTimeout(() => {
          if (thinkingScrollRef.current) {
            thinkingScrollRef.current.scrollTop = thinkingScrollRef.current.scrollHeight;
          }
        }, 100);
      } else {
        // 通常のツールアクティビティ
        setToolActivities(prev => [...prev, data.tool_activity!]);
      }
    }
    
    if (data.status === 'completed' && data.slides_html) {
      setSlidesHtml(data.slides_html);
      setIsResearching(false);
      toast.success('調査とスライド生成が完了しました！');
    } else if (data.status === 'error') {
      setIsResearching(false);
      toast.error(`エラー: ${data.error}`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      toast.error('調査内容を入力してください');
      return;
    }
    
    setIsResearching(true);
    setSlidesHtml(null);
    setToolActivities([]);
    setAgentThinking([]);
    
    try {
      const response = await axios.post(`${API_URL}/research`, {
        query,
        model_id: modelId,
        max_slides: maxSlides,
      });
      
      toast.info('調査を開始しました...');
    } catch (error) {
      setIsResearching(false);
      toast.error('リクエストの送信に失敗しました');
      console.error(error);
    }
  };

  const downloadSlides = () => {
    if (!slidesHtml) return;
    
    const blob = new Blob([slidesHtml], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `research_slides_${new Date().toISOString().slice(0, 10)}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <ToastContainer position="top-right" />
      
      {/* ヘッダー */}
      <header className="bg-purple-700 text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold flex items-center">
            <i className="fas fa-microscope mr-3"></i>
            Deep Research Slides Generator
          </h1>
          <p className="mt-2 text-purple-200">
            AIを使って詳細な調査を行い、美しいスライドを自動生成します
          </p>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-2 gap-8">
          {/* 入力フォーム */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              <i className="fas fa-search mr-2 text-purple-600"></i>
              調査リクエスト
            </h2>
            
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label className="block text-gray-700 font-bold mb-2">
                  調査内容
                </label>
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"
                  rows={4}
                  placeholder="例: 日本の電気自動車市場の現状と将来展望について"
                  disabled={isResearching}
                />
              </div>
              
              <div className="mb-6">
                <label className="block text-gray-700 font-bold mb-2">
                  使用モデル
                </label>
                <select
                  value={modelId}
                  onChange={(e) => setModelId(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"
                  disabled={isResearching}
                >
                  <option value="gpt-4o">GPT-4o</option>
                  <option value="gpt-4-turbo">GPT-4 Turbo</option>
                  <option value="claude-3-opus">Claude 3 Opus</option>
                  <option value="claude-3-sonnet">Claude 3 Sonnet</option>
                </select>
              </div>
              
              <div className="mb-6">
                <label className="block text-gray-700 font-bold mb-2">
                  最大スライド数
                </label>
                <input
                  type="number"
                  value={maxSlides}
                  onChange={(e) => setMaxSlides(parseInt(e.target.value))}
                  min={3}
                  max={10}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:border-purple-500"
                  disabled={isResearching}
                />
              </div>
              
              <button
                type="submit"
                disabled={isResearching}
                className={`w-full py-3 px-4 rounded-lg font-bold text-white transition-colors ${
                  isResearching
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-purple-600 hover:bg-purple-700'
                }`}
              >
                {isResearching ? (
                  <>
                    <i className="fas fa-spinner fa-spin mr-2"></i>
                    調査中...
                  </>
                ) : (
                  <>
                    <i className="fas fa-play mr-2"></i>
                    調査を開始
                  </>
                )}
              </button>
            </form>
          </div>

          {/* 進捗表示 */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              <i className="fas fa-tasks mr-2 text-purple-600"></i>
              進捗状況
            </h2>
            
            {currentResearch ? (
              <div>
                <div className="mb-4">
                  <div className="flex justify-between mb-2">
                    <span className="text-gray-700">
                      {currentResearch.message || 'waiting...'}
                    </span>
                    <span className="text-purple-600 font-bold">
                      {currentResearch.progress}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-purple-600 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${currentResearch.progress}%` }}
                    ></div>
                  </div>
                </div>
                
                {currentResearch.status === 'completed' && (
                  <div className="mt-6">
                    <button
                      onClick={downloadSlides}
                      className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-4 rounded-lg transition-colors"
                    >
                      <i className="fas fa-download mr-2"></i>
                      スライドをダウンロード
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">
                調査リクエストを送信すると、ここに進捗が表示されます
              </p>
            )}
          </div>

          {/* LLMの思考過程 */}
          {agentThinking.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6 mt-6 md:col-span-2">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold text-gray-800">
                  <i className="fas fa-brain mr-2 text-purple-600"></i>
                  AIの思考過程
                </h2>
                <button
                  onClick={() => setShowThinking(!showThinking)}
                  className="text-purple-600 hover:text-purple-800 font-medium"
                >
                  <i className={`fas fa-${showThinking ? 'eye-slash' : 'eye'} mr-2`}></i>
                  {showThinking ? '非表示' : '表示'}
                </button>
              </div>
              
              {showThinking && (
                <div
                  ref={thinkingScrollRef}
                  className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto font-mono text-sm"
                >
                  {agentThinking.map((thought, index) => (
                    <div
                      key={index}
                      className="mb-2 pb-2 border-b border-gray-200 last:border-b-0"
                    >
                      <pre className="whitespace-pre-wrap text-gray-700">
                        {thought}
                      </pre>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* 調査アクティビティ */}
          {toolActivities.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6 mt-6 md:col-span-2">
              <h2 className="text-2xl font-bold mb-6 text-gray-800">
                <i className="fas fa-globe mr-2 text-purple-600"></i>
                調査アクティビティ
              </h2>
              
              <div className="max-h-96 overflow-y-auto space-y-3">
                {toolActivities.map((activity, index) => (
                  <div
                    key={index}
                    className="border-l-4 border-purple-600 pl-4 py-2"
                  >
                    {activity.action === 'searching' && (
                      <div>
                        <div className="flex items-center text-blue-600">
                          <i className="fas fa-search mr-2"></i>
                          <span className="font-medium">検索中</span>
                        </div>
                        <p className="text-gray-700 ml-6">{activity.query}</p>
                      </div>
                    )}
                    
                    {activity.action === 'visiting' && (
                      <div>
                        <div className="flex items-center text-green-600">
                          <i className="fas fa-external-link-alt mr-2"></i>
                          <span className="font-medium">アクセス中</span>
                        </div>
                        <p className="text-gray-700 ml-6 truncate">
                          <a
                            href={activity.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-500 hover:underline"
                          >
                            {activity.url}
                          </a>
                        </p>
                      </div>
                    )}
                    
                    {activity.found_urls && activity.found_urls.length > 0 && (
                      <div className="ml-6 mt-2">
                        <p className="text-sm text-gray-600">見つかったURL:</p>
                        <ul className="list-disc list-inside text-sm">
                          {activity.found_urls.slice(0, 5).map((url, i) => (
                            <li key={i} className="text-gray-700 truncate">
                              <a
                                href={url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-500 hover:underline"
                              >
                                {url}
                              </a>
                            </li>
                          ))}
                          {activity.found_urls.length > 5 && (
                            <li className="text-gray-500">
                              他 {activity.found_urls.length - 5} 件...
                            </li>
                          )}
                        </ul>
                      </div>
                    )}
                    
                    {activity.error && (
                      <div className="text-red-600 ml-6">
                        <i className="fas fa-exclamation-triangle mr-2"></i>
                        {activity.error}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* スライドプレビュー */}
        {slidesHtml && (
          <div className="mt-8 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              <i className="fas fa-presentation mr-2 text-purple-600"></i>
              スライドプレビュー
            </h2>
            <div className="border border-gray-300 rounded-lg overflow-hidden">
              <iframe
                srcDoc={slidesHtml}
                className="w-full h-[800px]"
                title="Research Slides"
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;