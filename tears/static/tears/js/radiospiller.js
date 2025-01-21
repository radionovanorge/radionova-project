(function () {
	var Alien, Analyse, Music, con;

	Alien = (function () {
		class Alien {
			constructor() {
				this.getAlien = this.getAlien.bind(this);
				this.step = this.step.bind(this);
				this.halfColumns = this.numberOfColumns / 2;
				this.canvasWidth = this.cellSize * (this.numberOfColumns + 2);
				this.canvasHeight = this.cellSize * (this.numberOfRows + 2);
				this.canvas = document.createElement('canvas');
				this.drawingContext = this.canvas.getContext('2d');
				this.canvas.height = this.canvasWidth;
				this.canvas.width = this.canvasHeight;
				this.canvas.aliens = {
					x: 0,
					y: 0
				};
			}

			// console.log "canvas:::", @canvas
			clearCanvas() {
				return this.drawingContext.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
			}

			// @drawingContext.fillStyle = "red"
			// @drawingContext.fillRect 0,0, @canvasWidth, @canvasHeight
			seed() {
				var column, k, ref, results, row, seedCell;
				this.grid = [];
				results = [];
				for (row = k = 0, ref = this.numberOfRows;
					(0 <= ref ? k < ref : k > ref); row = 0 <= ref ? ++k : --k) {
					this.grid[row] = [];
					results.push((function () {
						var n, ref1, results1;
						results1 = [];
						for (column = n = 0, ref1 = this.halfColumns;
							(0 <= ref1 ? n < ref1 : n > ref1); column = 0 <= ref1 ? ++n : --n) {
							seedCell = this.createSeedCell(column);
							results1.push(this.grid[row][column] = seedCell);
						}
						return results1;
					}).call(this));
				}
				return results;
			}

			createSeedCell(probability) {
				var chance, cutoff, tobe;
				chance = Math.random();
				cutoff = (probability + 1) / (this.halfColumns + 1);
				tobe = chance < cutoff;
				// console.log chance, cutoff, tobe
				return tobe;
			}

			generateAlien() {
				var q, r;
				r = (m) => {
					return ~~(Math.random() * m + 1);
				};
				q = () => {
					var a, g, i, j, l;
					l = r(11);
					g = r(5);
					a = [];
					i = 0;
					while (i < l) {
						j = i * g;
						a.push(j);
						if (i) {
							a.unshift(-j);
						}
						i++;
					}
					return a;
				};
				return {
					x: q(),
					y: q()
				};
			}

			drawGrid(pixels) {
				var b, b1, colourFill, colourLine, column, g, g1, k, n, o, r, r1, ref, ref1, ref2, results, row;
				this.canvas.aliens = this.generateAlien();
				r = ~~(Math.random() * 128 + 64);
				g = ~~(Math.random() * 128 + 64);
				b = ~~(Math.random() * 128 + 64);
				colourLine = `rgba(${r}, ${g}, ${b}, 1)`;
				r1 = ~~(r - Math.random() * 64);
				g1 = ~~(g - Math.random() * 64);
				b1 = ~~(b - Math.random() * 64);
				colourFill = `rgb(${r1}, ${g1}, ${b1})`;
				for (row = k = 0, ref = this.numberOfRows;
					(0 <= ref ? k < ref : k > ref); row = 0 <= ref ? ++k : --k) {
					for (column = n = 0, ref1 = this.numberOfColumns;
						(0 <= ref1 ? n < ref1 : n > ref1); column = 0 <= ref1 ? ++n : --n) {
						this.drawCell(row, column, colourLine, 10);
					}
				}
				results = [];
				for (row = o = 0, ref2 = this.numberOfRows;
					(0 <= ref2 ? o < ref2 : o > ref2); row = 0 <= ref2 ? ++o : --o) {
					results.push((function () {
						var p, ref3, results1;
						results1 = [];
						for (column = p = 0, ref3 = this.numberOfColumns;
							(0 <= ref3 ? p < ref3 : p > ref3); column = 0 <= ref3 ? ++p : --p) {
							results1.push(this.drawCell(row, column, colourFill, 0));
						}
						return results1;
					}).call(this));
				}
				return results;
			}

			drawCell(y, x, fillStyle, strokeWidth) {
				var colReflected, isOn;
				if (x >= this.halfColumns) {
					colReflected = this.numberOfColumns - x - 1;
				} else {
					colReflected = x;
				}
				isOn = this.grid[y][colReflected];
				if (isOn) {
					this.drawingContext.fillStyle = fillStyle;
					return this.drawingContext.fillRect((1 + x) * this.cellSize - strokeWidth, (1 + y) * this.cellSize - strokeWidth, this.cellSize + strokeWidth * 2, this.cellSize + strokeWidth * 2);
				}
			}

			getAlien() {
				// console.log "getAlien", @canvas
				return this.canvas;
			}

			step() {}

			// if @ticks % 40 == 0
			//   @change()
			// @ticks++
			change() {
				this.clearCanvas();
				this.seed();
				return this.drawGrid();
			}

		};

		Alien.prototype.grid = null;

		Alien.prototype.cellSize = 30;

		Alien.prototype.numberOfRows = 10;

		Alien.prototype.numberOfColumns = 10;

		Alien.prototype.halfColumns = 0;

		Alien.prototype.colReflected = 0;

		Alien.prototype.ticks = 0;

		Alien.prototype.canvas = null;

		Alien.prototype.drawingContext = null;

		Alien.prototype.canvasWidth = 0;

		Alien.prototype.canvasHeight = 0;

		return Alien;

	}).call(this);

	window.Alien = Alien;

	con = console;

	class AudioAnalyzer {
		constructor() {
			this.initializeAudioContext();
			this.setupEventListeners();
			this.isPlaying = false;
		}
	
		initializeAudioContext() {
			// Create or reuse AudioContext
			if (!window.globalAudioContext) {
				window.globalAudioContext = new (window.AudioContext || window.webkitAudioContext)();
			}
			this.audioContext = window.globalAudioContext;
	
			// Create AnalyserNode
			this.analyser = this.audioContext.createAnalyser();
			this.analyser.fftSize = 2048; // Power of 2, bigger = more detailed
			this.analyser.smoothingTimeConstant = 0.8;
	
			// Create buffers for analysis
			this.frequencyData = new Uint8Array(this.analyser.frequencyBinCount);
			this.timeData = new Uint8Array(this.analyser.frequencyBinCount);
		}
	
		setupEventListeners() {
			this.audioElement = document.getElementById('radio-player');
			
			if (!this.audioElement) {
				console.error('Audio element not found');
				return;
			}
	
			// Create and connect nodes only when starting playback
			this.audioElement.addEventListener('play', () => {
				if (!this.sourceNode) {
					this.sourceNode = this.audioContext.createMediaElementSource(this.audioElement);
					this.sourceNode.connect(this.analyser);
					this.analyser.connect(this.audioContext.destination);
				}
				this.isPlaying = true;
				this.startVisualization();
			});
	
			this.audioElement.addEventListener('pause', () => {
				this.isPlaying = false;
			});
		}
	
		analyze() {
			// Get frequency and time domain data
			this.analyser.getByteFrequencyData(this.frequencyData);
			this.analyser.getByteTimeDomainData(this.timeData);
	
			// Calculate average amplitude
			let sum = 0;
			for (let i = 0; i < this.frequencyData.length; i++) {
				sum += this.frequencyData[i];
			}
			const average = sum / this.frequencyData.length;
	
			return {
				frequency: Array.from(this.frequencyData),
				waveform: Array.from(this.timeData),
				amplitude: average / 255 // Normalize to 0-1
			};
		}
	
		startVisualization() {
			const canvas = document.querySelector('#visualizer-container canvas');
			if (!canvas) return;
	
			const ctx = canvas.getContext('2d');
			const draw = () => {
				if (!this.isPlaying) return;
	
				const analysis = this.analyze();
				
				// Clear canvas
				ctx.clearRect(0, 0, canvas.width, canvas.height);
	
				// Draw frequency bars
				const barWidth = canvas.width * 4 / analysis.frequency.length;
				const heightMultiplier = canvas.height / 355;
	
				ctx.fillStyle = '#FF0000';
				analysis.frequency.forEach((value, i) => {
					const height = value * heightMultiplier;
					ctx.fillRect(
						i * barWidth, 
						canvas.height - height,
						barWidth - 1,
						height
					);
				});
	
				// Draw waveform
				ctx.beginPath();
				ctx.strokeStyle = '#FF0000';
				ctx.lineWidth = 1;
				analysis.waveform.forEach((value, i) => {
					const x = i * (canvas.width / analysis.waveform.length);
					const y = (value / 255) * canvas.height;
					if (i === 0) {
						ctx.moveTo(x, y);
					} else {
						ctx.lineTo(x, y);
					}
				});
				ctx.stroke();
	
				requestAnimationFrame(draw);
			};
	
			requestAnimationFrame(draw);
		}
	}

	window.Analyse = Analyse;


	//------------------------------------------//
	//-------- STUFF FOR AUDIO ANALYSIS --------//
	function FourierTransform(bufferSize, sampleRate) {
		this.bufferSize = bufferSize;
		this.sampleRate = sampleRate;
		this.bandwidth = bufferSize * sampleRate;
		this.spectrum = new Float32Array(bufferSize / 2);
		this.real = new Float32Array(bufferSize);
		this.imag = new Float32Array(bufferSize);
		this.peakBand = 0;
		this.peak = 0;
		this.getBandFrequency = function (index) {
			return this.bandwidth * index + this.bandwidth / 2;
		};
		this.calculateSpectrum = function () {
			var spectrum = this.spectrum,
				real = this.real,
				imag = this.imag,
				bSi = 2 / this.bufferSize,
				rval, ival, mag;
			this.peak = this.peakBand = 0;
			for (var i = 0, N = bufferSize * 0.5; i < N; i++) {
				rval = real[i];
				ival = imag[i];
				mag = bSi * Math.sqrt(rval * rval + ival * ival);
				if (mag > this.peak) {
					this.peakBand = i;
					this.peak = mag;
				}
				spectrum[i] = mag;
			}
		};
	}

	function FFT(bufferSize, sampleRate) {
		FourierTransform.call(this, bufferSize, sampleRate);
		this.reverseTable = new Uint32Array(bufferSize);
		var limit = 1;
		var bit = bufferSize >> 1;
		var i;
		while (limit < bufferSize) {
			for (i = 0; i < limit; i++)
				this.reverseTable[i + limit] = this.reverseTable[i] + bit;
			limit = limit << 1;
			bit = bit >> 1;
		}
		this.sinTable = new Float32Array(bufferSize);
		this.cosTable = new Float32Array(bufferSize);
		for (i = 0; i < bufferSize; i++) {
			this.sinTable[i] = Math.sin(-Math.PI / i);
			this.cosTable[i] = Math.cos(-Math.PI / i);
		}
	}
	FFT.prototype.forward = function (buffer) {
		var bufferSize = this.bufferSize,
			cosTable = this.cosTable,
			sinTable = this.sinTable,
			reverseTable = this.reverseTable,
			real = this.real,
			imag = this.imag,
			spectrum = this.spectrum;
		var k = Math.floor(Math.log(bufferSize) / Math.LN2);
		if (Math.pow(2, k) !== bufferSize) {
			throw "Invalid buffer size, must be a power of 2.";
		}
		if (bufferSize !== buffer.length) {
			throw "Supplied buffer is not the same size as defined FFT. FFT Size: " + bufferSize + " Buffer Size: " + buffer.length;
		}
		var halfSize = 1,
			phaseShiftStepReal,
			phaseShiftStepImag,
			currentPhaseShiftReal,
			currentPhaseShiftImag,
			off,
			tr,
			ti,
			tmpReal,
			i;
		for (i = 0; i < bufferSize; i++) {
			real[i] = buffer[reverseTable[i]];
			imag[i] = 0;
		}
		while (halfSize < bufferSize) {
			phaseShiftStepReal = cosTable[halfSize];
			phaseShiftStepImag = sinTable[halfSize];
			currentPhaseShiftReal = 1;
			currentPhaseShiftImag = 0;
			for (var fftStep = 0; fftStep < halfSize; fftStep++) {
				i = fftStep;
				while (i < bufferSize) {
					off = i + halfSize;
					tr = (currentPhaseShiftReal * real[off]) - (currentPhaseShiftImag * imag[off]);
					ti = (currentPhaseShiftReal * imag[off]) + (currentPhaseShiftImag * real[off]);
					real[off] = real[i] - tr;
					imag[off] = imag[i] - ti;
					real[i] += tr;
					imag[i] += ti;
					i += halfSize << 1;
				}
				tmpReal = currentPhaseShiftReal;
				currentPhaseShiftReal = (tmpReal * phaseShiftStepReal) - (currentPhaseShiftImag * phaseShiftStepImag);
				currentPhaseShiftImag = (tmpReal * phaseShiftStepImag) + (currentPhaseShiftImag * phaseShiftStepReal);
			}
			halfSize = halfSize << 1;
		}
		return this.calculateSpectrum();
	};

	window.FFT = FFT;;

	con = console;

	Music = (function () {
		class Music {
			constructor() {
				this.step = this.step.bind(this);
				con.log("Music constructor");
				this.createCanvas();
				this.analyser = new Analyse(this.pixels, this.centreX, this.centreY);
				this.aliendude = new Alien();
				if (window.requestAnimationFrame) {
					con.log("native requestAnimationFrame");
				} else {
					con.log("creating requestAnimationFrame");
					window.requestAnimationFrame = window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame;
				}
				// function(callback, element){
				//  window.setTimeout(callback, 1000 / 60);
				// };
				this.step();
			}

			createCanvas() {
				// Set canvas dimensions and properties
				this.canvasWidth = 300; // Width of the visualizer container
				this.canvasHeight = 80; // Height to match navbar
				this.centreX = this.canvasWidth / 2;
				this.centreY = this.canvasHeight / 2;

				// Create and configure the canvas element
				this.canvas = document.createElement('canvas');
				this.canvas.style.width = '100%';
				this.canvas.style.height = '100%';

				// Set the actual canvas resolution
				this.canvas.width = this.canvasWidth;
				this.canvas.height = this.canvasHeight;

				// Get the container and append the canvas
				const container = document.getElementById('visualizer-container');
				if (container) {
					container.appendChild(this.canvas);
				}

				// Get the drawing context
				this.pixels = this.canvas.getContext('2d');
			}


			clearCanvas() {
				//pixels.globalCompositeOperation = 'source-atop'
				this.pixels.fillStyle = "rgb(0, 0, 0)";
				//@pixels.fillStyle = "rgba(0, 0, 0, 0.4)"
				return this.pixels.clearRect(0, 0, this.canvasWidth, this.canvasHeight); // Clear the entire canvas
			}

			step() {
				var amplitude, anal, b, bandWidth, c, g, i, img, k, len, len1, level, n, o, p, padding, r, ref, ref1, ref2, ref3, sc, specLength, spectrum, waveform, waveformLength, x, y;
				this.clearCanvas();
				this.analyser.step();
				this.aliendude.step();
				anal = this.analyser.getAnalysis();
				spectrum = anal.spectrum;
				amplitude = anal.amplitude;
				waveform = anal.waveform;
				//draw amplitude
				this.pixels.fillStyle = "transparent"; //anylyser background
				this.pixels.fillRect(0, this.canvasHeight, this.canvasWidth, -amplitude * this.canvasHeight);
				//draw spectrum
				specLength = spectrum.length;
				bandWidth = this.canvasWidth / specLength;
				padding = 5;
				for (i = k = 0, ref = specLength;
					(0 <= ref ? k < ref : k > ref); i = 0 <= ref ? ++k : --k) {
					c = ~~(i / specLength * 55);
					r = 100;
					g = 200 + c;
					b = 255 - c;
					level = spectrum[i];
					this.pixels.fillStyle = `#FF0000`;
					this.pixels.fillRect(i * bandWidth + padding, this.canvasHeight, bandWidth - padding * 2, -level * this.centreY * 0.5);
				}
				// draw waveform
				waveformLength = waveform.length;
				bandWidth = this.canvasWidth / waveformLength;
				this.pixels.beginPath();
				for (i = n = 0, ref1 = waveformLength;
					(0 <= ref1 ? n < ref1 : n > ref1); i = 0 <= ref1 ? ++n : --n) {
					//@pixels.fillStyle = "rgba(255, 255, 255, 0.5)"
					//@pixels.fillRect( i * bandWidth, @centreY, bandWidth, waveform[i] * @centreY)
					this.pixels.strokeStyle = '#FF0000'; //waveformen farge
					this.pixels.lineWidth = 1;
					x = i * bandWidth;
					y = this.centreY + waveform[i] * this.centreY;
					if (i === 0) {
						this.pixels.moveTo(x, y);
					} else {
						this.pixels.lineTo(x, y);
					}
				}
				this.pixels.stroke();
				this.float += this.alienRotate;
				//@scale += 0.01
				this.scale = spectrum[0];
				if (this.scale > this.alienScale * 4) {
					this.aliendude.change();
					this.alienScale = this.scale;
					this.alienRotate = (Math.random() - 0.5) * 0.1;
				} else {
					this.alienScale *= 0.9;
				}

				this.pixels.restore();
				// attempt at 3d, but shearing of only 2 triangle subdivisions and this will get costly really fast.
				// corners = [
				//   {x:100,y:100,u:0,v:0},
				//   {x:300,y:50,u:img.width,v:0},
				//   {x:350,y:300,u:img.width,v:img.height},
				//   {x:200,y:400,u:0,v:img.height}
				// ]

				// for c in corners
				//   @pixels.fillStyle = "#f00"
				//   @pixels.fillRect( c.x, c.y, 5, 5 )

				// textureMap( @pixels, img, corners )
				return requestAnimationFrame(this.step);
			}

		};

		Music.prototype.analyser = null;

		Music.prototype.aliendude = null;

		Music.prototype.canvas = null;

		Music.prototype.pixels = null;

		Music.prototype.canvasWidth = 1000;

		Music.prototype.canvasHeight = 500;

		Music.prototype.centreX = 0;

		Music.prototype.centreY = 0;

		Music.prototype.scale = 1;

		Music.prototype.float = 20;

		//@pixels.globalCompositeOperation = 'lighter'
		Music.prototype.alienScale = 2;

		Music.prototype.alienRotate = 0.01;

		return Music;

	}).call(this);


	window.Music = Music;
    window.musicVisualizer = null; // Store single instance

    window.toggleRadio = function() {
		const radioPlayer = document.getElementById('radio-player');
		const playIcon = document.getElementById('play-radio-icon');
		const playText = document.getElementById('play-text');
	
		if (!window.audioAnalyzer) {
			window.audioAnalyzer = new AudioAnalyzer();
		}
	
		if (radioPlayer.paused) {
			// Check if already attempting to play
			if (radioPlayer.readyState >= 2) { // Ensure the audio is ready to play
				radioPlayer.play()
					.then(() => {
						playIcon.className = 'fa fa-pause fa-xl';
						playText.textContent = 'Pause';
					})
					.catch(error => {
						console.error('Error playing audio:', error);
					});
			} else {
				console.warn('Audio not ready to play.');
			}
		} else {
			radioPlayer.pause();
			playIcon.className = 'fa fa-play fa-xl';
			playText.textContent = 'Play';
		}
	};

}).call(this);