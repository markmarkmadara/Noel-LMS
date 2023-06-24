<script setup>
import tomatoLogo from '@/assets/icons/tomato.svg'
// grab everything we need
const btn = document.querySelector('button.mobile-menu-button')
const menu = document.querySelector('.mobile-menu')

// add event listeners
window.onload = function () {
  const btn = document.querySelector('button.mobile-menu-button')
  const menu = document.querySelector('.mobile-menu')
  btn.addEventListener('click', () => {
    menu.classList.toggle('hidden')
  })
}
</script>

<template>
  <div class="bg-gray-500">
    <nav class="bg-gray-100">
      <div class="max-w-6xl mx-auto px-4">
        <div class="flex justify-between">
          <div class="flex space-x-4">
            <!-- logo -->
            <div>
              <a
                href="#"
                class="flex items-center py-5 px-2 text-gray-700 hover:text-gray-900"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  class="logo z-depth-3"
                  width="80px"
                  height="80px"
                  viewBox="0 -5 80 80"
                >
                  <g transform="translate(10)">
                    <path
                      d="m58.982 34.35c0 16.287-13.2 29.489-29.491 29.489-16.289.0001-29.491-13.201-29.491-29.489 0-16.292 13.202-17.909 29.491-17.909 16.291 0 29.491 1.617 29.491 17.909"
                      fill="#be202e"
                      class="red-shadow"
                    ></path>
                    <path
                      d="m27.752 31.969c-.396.461-.785.952-1.191 1.511-.738 1.036-2.433 1.6-3.4.439-1.822-2.196-2.935-4.24-3.87-6.702-3.02.482-5.905.872-9.04.838-1.541-.017-2.835-1.866-1.871-3.264 1.798-2.603 3.76-4.807 5.935-7.118.083-.084.171-.11.256-.177-8.709 1.692-14.57 6.02-14.57 16.859 0 16.287 13.202 29.489 29.491 29.489 6.611 0 12.692-2.201 17.609-5.874-8.888-6.079-15.757-16.366-19.348-26"
                      fill="#9b1f2e"
                    ></path>
                    <g fill="#04a69c">
                      <path
                        d="m38.803 14.838c3.4-.482 9.578 8.196 9.919 10.587.338 2.388-6.669.64-10.634.158-4.088-.497-8.246-.784-8.584-3.171-.338-2.386 5.911-7.091 9.299-7.574"
                      ></path>
                      <path
                        d="m18.898 14.838c-3.394-.482-9.572 8.196-9.913 10.587-.338 2.388 6.663.64 10.636.158 4.085-.497 8.243-.784 8.581-3.171.34-2.386-5.91-7.091-9.304-7.574"
                      ></path>
                    </g>
                    <path
                      d="m22.719 21.875c-1.866 1.663.199 9.226 1.401 10.546 1.206 1.32 3.489-3.406 5.073-5.848 1.629-2.514 3.415-4.969 2.209-6.289-1.206-1.324-6.825-.072-8.683 1.591"
                      fill="#2bb573"
                    ></path>
                    <path
                      d="m28.336 11.644c1.449-2.035 9.193-.812 10.636.241 1.445 1.054-3.01 3.842-5.26 5.679-2.318 1.9-4.559 3.939-6.01 2.886-1.443-1.054-.817-6.775.632-8.806"
                      fill="#038d80"
                    ></path>
                    <path
                      d="m29.16.828c.23.173.192 1.942.125 2.09-1.733 3.753.778 13.333 1.202 14.67.979 3.102.19 6.8-1.398 6.546-1.53-.246-4.371-6.445-4.989-7.667-1.511-3-2.302-6.897-2.094-10.257.212-3.541 3.532-8.103 7.154-5.382"
                      fill="#2bb573"
                    ></path>
                  </g>
                </svg>
                <span id="textTomatoLogo" class="font-bold">TomatoCare</span>
              </a>
            </div>

            <!-- primary nav -->
            <div class="hidden md:flex items-center space-x-1">
              <a href="#" class="py-5 px-3 text-gray-700 hover:text-red-500"
                >Home</a
              >
              <a href="#" class="py-5 px-3 text-gray-700 hover:text-red-500"
                >About</a
              >
            </div>
          </div>

          <!-- secondary nav -->
          <div class="hidden md:flex items-center space-x-1">
            <a href="/login" class="py-5 px-3 text-gray-700 hover:text-red-500"
              >Login</a
            >
            <a
              href=""
              class="py-2 px-3 bg-red-800 hover:bg-red-600 text-gray-100 hover:text-gray-200 rounded transition duration-300"
              >Signup</a
            >
          </div>

          <!-- mobile button goes here -->
          <div class="md:hidden flex items-center">
            <button class="mobile-menu-button">
              <svg
                class="w-6 h-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 12h16M4 18h16"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- mobile menu -->
      <div class="mobile-menu hidden md:hidden">
        <a href="#" class="block py-2 px-4 text-lg hover:bg-gray-200">Home</a>
        <a href="#" class="block py-2 px-4 text-lg hover:bg-gray-200">About</a>
        <a href="#" class="block py-2 px-4 text-lg hover:bg-gray-200">Login</a>
        <a
          href="#"
          class="block py-2 px-4 text-sm bg-yellow-400 hover:bg-yellow-300 text-yellow-900 hover:text-yellow-800 rounded transition duration-300"
          >Signup</a
        >
      </div>
    </nav>
  </div>
</template>

<style scoped>
nav {
  font-family: 'Poppins', sans-serif;
  font-size: 1.2rem;
  font-weight: 500;
}

#textTomatoLogo {
  margin: 0.5em;
  position: relative;
  font-family: 'EB Garamond', 'serif';
  font-size: 2rem;
  transition: all 0.5s ease-in-out;
}

#textTomatoLogo:hover {
  text-shadow: 0 10px 10px rgba(0, 0, 0, 0.2);
  color: rgb(255, 0, 0);
}
</style>
