/* eslint-disable react/prop-types */

import { useEffect, useRef, useState } from "react"
import RobotControlPanel from "./RobotController";
import SettingsPopup from "./SettingsPopup";

export const LOCALSTORAGE = "ee31-client-settings";
const DEFAULT_SETTINGS = {
  f_fwd: "f_fwd",
  s_fwd: "s_fwd",
  f_lft: "f_lft",
  s_lft: "s_lft",
  f_rht: "f_rht",
  s_rht: "s_rht",
  f_bwd: "f_bwd",
  s_bwd: "s_bwd",
  stop: "stop",
  red: "color.red",
  yellow: "color.yellow",
  blue: "color.blue",
  collision: "collision",
  night: "night",
  day: "day",
  buzzer: "buzzer",
  custom1: "undefined",
  custom2: "undefined",
  custom3: "undefined",
  custom4: "undefined"

}

export default function WebSocketLog(props) {
  const messagesRef = useRef(null);
  const [messageInput, setMessageInput] = useState("");
  const [settings, setSettings] = useState();

  const handleChange = event => {
    setMessageInput(event.target.value);
  }


  useEffect(() => {
    messagesRef.current.scroll({ top: messagesRef.current.scrollHeight, behavior: 'smooth' });
    console.log(props.log.length)
  }, [props, props.log])

  useEffect(() => {
    if (!localStorage.getItem(LOCALSTORAGE)) {
      resetSettings();
    }
    else {
      setSettings(JSON.parse(localStorage.getItem(LOCALSTORAGE)));
    }
  }, [])

  function resetSettings() {
    localStorage.setItem(LOCALSTORAGE, JSON.stringify(DEFAULT_SETTINGS));
    setSettings(DEFAULT_SETTINGS);
  }

  return (
    <>
      <div className="bg-white shadow-lg rounded-lg p-8 m-4 w-full max-w-5xl block">

        <h2 className="font-bold text-2xl mb-4"> Simple Frontend Interface ({props.connected ? "Connected" : "Not Connected"})</h2>
        <div className="absolute right-2 top-2">
          <SettingsPopup settings={settings} setSettings={setSettings} resetSettings={resetSettings} />
        </div>

        <div className="lg:grid lg:grid-cols-2">
          <div className="block">
            <RobotControlPanel sendMessage={props.sendMessage} settings={settings} />
          </div>
          <div className="w-full bg-white shadow rounded">
            <div className="p-4">
              <h2 className="font-semibold text-lg">Log of Server Messages</h2>
            </div>
            <div className="overflow-auto h-64 md:h-72 lg:min-h-80" style={{ scrollBehavior: "smooth" }} ref={messagesRef}>
              {props.log.map((item, index) => (
                <div key={index} className="p-2 border-b border-gray-200">
                  {item}
                </div>
              ))}
              <div />
            </div>


            <div className="mx-4 py-2">
              <form className="md:inline" onSubmit={(e) => {
                e.preventDefault();
                props.sendMessage(messageInput);
                setMessageInput("");
              }}>
                <label className="">Input:</label>
                <input
                  id="id-01"
                  type="text"
                  name="id-01"
                  placeholder="Enter a message here..."
                  value={messageInput}
                  className="peer md:inline h-10 w-full rounded border border-slate-200 px-4 text-sm text-slate-500 placeholder-transparent outline-none transition-all autofill:bg-white invalid:border-pink-500 invalid:text-pink-500 focus:border-blue-500 focus:outline-none invalid:focus:border-pink-500 focus-visible:outline-none disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400 my-3"
                  onChange={handleChange}
                />


              </form>

            </div>

          </div>

        </div>
        <div className="flex justify-center p-4">

        </div>

      </div>
    </>
  )
}