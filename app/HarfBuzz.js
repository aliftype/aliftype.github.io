/*
 * Copyright (c) 2019-2021 Khaled Hosny
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 *
 * Copyright (c) 2019 Ebrahim Byagowi
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

import { GSUB, TAG } from "./OpenType.js"

class Pointer {
  constructor(arg) {
    if (arg instanceof ArrayBuffer) {
      this.byteLength = arg.byteLength;
      this.ptr = M._malloc(this.byteLength);
      M.HEAPU8.set(new Uint8Array(arg), this.ptr);
    } else {
      this.byteLength = arg;
      this.ptr = M._malloc(this.byteLength);
    }
  }

  get int32Array() { return M.HEAP32.slice(this.ptr / 4, (this.ptr + this.byteLength) / 4); }
  get uint32Array() { return M.HEAPU32.slice(this.ptr / 4, (this.ptr + this.byteLength) / 4); }
  get int32() { return M.HEAP32[this.ptr / 4]; }
  set int32(value) { M.HEAP32[this.ptr / 4] = value; }
  get uint32() { return M.HEAPU32[this.ptr / 4]; }
  set uint32(value) { M.HEAPU32[this.ptr / 4] = value; }

  release() {
    M._free(this.ptr);
  }
}

export class Color {
  constructor(color) {
    this._color = color;
  }

  get red() { return M._hb_color_get_red(this._color); }
  get green() { return M._hb_color_get_green(this._color); }
  get blue() { return M._hb_color_get_blue(this._color); }
  get alpha() { return M._hb_color_get_alpha(this._color); }
}

export class Font {
  constructor(data, dpr) {
    let dataPtr = new Pointer(data);
    let blob = M._hb_blob_create(dataPtr.ptr, dataPtr.byteLength, 0/*HB_MEMORY_MODE_DUPLICATE*/, 0, 0);
    dataPtr.release();
    this.face = M._hb_face_create(blob, 0);
    this.ptr = M._hb_font_create(this.face);
    this.upem = M._hb_face_get_upem(this.face);

    let scale = this.upem * dpr;
    M._hb_font_set_scale(this.ptr, scale, scale);

    this._outlines = [];
    this._glyph_extents = [];
    this._color_layers = [];
    this._color_palettes = [];
    this._font_extents = undefined;
    this._gsub = undefined;
    this._draw_funcs = null;
  }

  getGlyphExtents(glyph) {
    if (this._glyph_extents[glyph] == undefined) {
      let extentsPtr = new Pointer(4 * 4);
      M._hb_font_get_glyph_extents(this.ptr, glyph, extentsPtr.ptr);

      let extents = extentsPtr.int32Array;
      this._glyph_extents[glyph] = {
        x_bearing: extents[0],
        y_bearing: extents[1],
        width: extents[2],
        height: extents[3],
      };
      extentsPtr.release();
    }

    return this._glyph_extents[glyph];
  }

  _getColorPalette(index) {
    if (!M._hb_ot_color_has_palettes(this.face))
      return null;

    if (this._color_palettes[index] == undefined) {
      let numColorsPtr = new Pointer(4);
      numColorsPtr.uint32 = M._hb_ot_color_palette_get_colors(this.face, index, 0, 0, 0);
      let colorsPtr = new Pointer(numColorsPtr.uint32 * 4);
      M._hb_ot_color_palette_get_colors(this.face, index, 0, numColorsPtr.ptr, colorsPtr.ptr);
      let palette = [];
      colorsPtr.uint32Array.forEach(x => palette.push(new Color(x)));
      this._color_palettes[index] = palette;
      colorsPtr.release();
      numColorsPtr.release();
    }
    return this._color_palettes[index];
  }

  getGlyphColorLayers(glyph) {
    if (!M._hb_ot_color_has_layers(this.face))
      return;

    let palette = this._getColorPalette(0);

    if (this._color_layers[glyph] == undefined) {
      let numLayersPtr = new Pointer(4);
      numLayersPtr.uint32 = M._hb_ot_color_glyph_get_layers(this.face, glyph, 0, 0, 0);
      if (numLayersPtr.uint32 == 0) {
        numLayersPtr.release();
        return;
      }
      let layersPtr = new Pointer(numLayersPtr.uint32 * 8);

      M._hb_ot_color_glyph_get_layers(this.face, glyph, 0, numLayersPtr.ptr, layersPtr.ptr);

      let layers = layersPtr.uint32Array;
      this._color_layers[glyph] = [];
      for (let i = 0; i < numLayersPtr.uint32; i++) {
        this._color_layers[glyph].push({
          index: layers[i * 2],
          color: palette[layers[i * 2 + 1]],
        });
      }
      layersPtr.release();
      numLayersPtr.release();
    }
    return this._color_layers[glyph];
  }

  getGlyphOutline(glyph) {
    let outlines = this._outlines;
    if (outlines[glyph] !== undefined)
      return outlines[glyph];

    if (!this._draw_funcs) {
      let funcs = this._draw_funcs = M._hb_draw_funcs_create();
      let move_to = M.addFunction(function (f, g, s, x, y, u) {
        outlines[g] += `M${x},${-y}`;
      }, "viiiffi");
      let line_to = M.addFunction(function (f, g, s, x, y, u) {
        outlines[g] += `L${x},${-y}`;
      }, "viiiffi");
      let quadratic_to = M.addFunction(function (f, g, s, x1, y1, x2, y2, u) {
        outlines[g] += `Q${x1},${-y1},${x2},${-y2}`;
      }, "viiiffffi");
      let cubic_to = M.addFunction(function (f, g, s, x1, y1, x2, y2, x3, y3, u) {
        outlines[g] += `C${x1},${-y1},${x2},${-y2},${x3},${-y3}`;
      }, "viiiffffffi");
      let close_path = M.addFunction(function (f, g, s, u) {
        outlines[g] += `Z`
      }, "viiii");

      M._hb_draw_funcs_set_move_to_func(funcs, move_to, 0, 0);
      M._hb_draw_funcs_set_line_to_func(funcs, line_to, 0, 0);
      M._hb_draw_funcs_set_quadratic_to_func(funcs, quadratic_to, 0, 0);
      M._hb_draw_funcs_set_cubic_to_func(funcs, cubic_to, 0, 0);
      M._hb_draw_funcs_set_close_path_func(funcs, close_path, 0, 0);
    }

    outlines[glyph] = "";
    // I’m abusing pointers here to pass the actual glyph id instead of a user
    // data pointer, don’t shoot me.
    M._hb_font_draw_glyph(this.ptr, glyph, this._draw_funcs, glyph);

    return outlines[glyph];
  }

  _getTable(name, klass) {
    let lenPtr = new Pointer(4);
    let blob = M._hb_face_reference_table(this.face, TAG(name));
    let data = M._hb_blob_get_data(blob, lenPtr.ptr);
    let table = null
    if (lenPtr.uint32 != 0)
      table = new klass(M.HEAPU8.slice(data, data + lenPtr.uint32));
    lenPtr.release();
    return table;
  }

  get GSUB() {
    if (!this._gsub) this._gsub = this._getTable("GSUB", GSUB);
    return this._gsub;
  }

  getAlternates(lookupIndex, glyph, next) {
    let lookup = this.GSUB.lookup(lookupIndex);

    if (next) {
      let res = lookup.mapping[[glyph, next]];
      if (res)
        return res;
    }

    return lookup.mapping[glyph];
  }

  get extents() {
    if (this._font_extents == undefined) {
      let extentsPtr = new Pointer(12 * 4);
      M._hb_font_get_h_extents(this.ptr, extentsPtr.ptr);
      let extents = extentsPtr.int32Array;
      let clipAscender = extents[0];
      let clipDescender = extents[1];
      let clipPtr = new Pointer(4);
      if (M._hb_ot_metrics_get_position(this.ptr, TAG("hcla"), clipPtr.ptr))
        clipAscender = clipPtr.int32;
      if (M._hb_ot_metrics_get_position(this.ptr, TAG("hcld"), clipPtr.ptr))
        clipDescender = clipPtr.int32;

      this._font_extents = {
        ascender: extents[0],
        descender: extents[1],
        line_gap: extents[2],
        clipAscender: clipAscender,
        clipDescender: clipDescender,
      };

      extentsPtr.release();
      clipPtr.release();
    }
    return this._font_extents;
  }
}

let ALTERNATE_FEATURES = ["salt", "dlig"].concat(
  [...Array(100).keys()].map(
    i => `cv${String(i).padStart(2, '0')}`
  )
);

class Glyph {
  constructor(font, info, position) {
    this.font = font;
    this.index = info[0];
    this.cl = info[2];
    this.ax = position[0];
    this.ay = position[1];
    this.dx = position[2];
    this.dy = position[3];

    this._alternates = null;
  }

  get isDot() {
    return !!this.font.getGlyphColorLayers(this.index);
  }

  get layers() {
    let layers = this.font.getGlyphColorLayers(this.index);
    if (!layers)
      return;
    return layers.map(l => {
      let glyph = { ...this, index: l.index, color: l.color };
      Object.setPrototypeOf(glyph, Glyph.prototype);
      return glyph;
    });
  }
  get outline() { return this.font.getGlyphOutline(this.index); }

  getAlternates(next) {
    if (this._alternates === null) {
      let features = this.font.GSUB.features;
      let result = new Set();
      for (const [tag, lookups] of Object.entries(features)) {
        if (ALTERNATE_FEATURES.includes(tag)) {
          for (const lookup of lookups) {
            let alternates = this.font.getAlternates(lookup, this.index, next && next.index);
            if (alternates)
              result.add([tag, [this.index, ...alternates]]);
          }
        }
      }
      this._alternates = result.size && Array.from(result) || undefined;
    }
    return this._alternates;
  }
}

export class Buffer {
  constructor() { this.ptr = M._hb_buffer_create(); }

  shape(font, text, useFeatures, globalFeatures) {
    M._hb_buffer_clear_contents(this.ptr);
    M._hb_buffer_set_direction(this.ptr, 5/*rtl*/);
    M._hb_buffer_set_script(this.ptr, TAG("Arab"));
    M._hb_buffer_set_content_type(this.ptr, 1/*unicode*/);

    let features = [];
    for (let i = 0; i < text.length; i++) {
      M._hb_buffer_add(this.ptr, text[i].code, i);
      for (const feature of text[i].features || []) {
        let [tag, value] = feature.split("=");
        value = value ? parseInt(value) : 1;
        if (useFeatures || tag == "dlig") {
          features.push(TAG(feature), value, i, i + 1);
        }
      }
    }

    for (const feature of globalFeatures) {
      features.push(TAG(feature), 1, 0, -1);
    }

    let featuresPtr = new Pointer(new Uint32Array(features).buffer);
    M._hb_shape(font.ptr, this.ptr, featuresPtr.ptr, features.length / 4);
    featuresPtr.release();

    let length = M._hb_buffer_get_length(this.ptr);
    let infosPtr32 = M._hb_buffer_get_glyph_infos(this.ptr, 0) / 4;
    let positionsPtr32 = M._hb_buffer_get_glyph_positions(this.ptr, 0) / 4;
    let infos = M.HEAPU32.slice(infosPtr32, infosPtr32 + 5 * length);
    let positions = M.HEAP32.slice(positionsPtr32, positionsPtr32 + 5 * length);
    let glyphs = [];
    for (let i = 0; i < length; ++i) {
      let j = i * 5;
      let info = infos.slice(j, j + 5);
      let position = positions.slice(j, j + 5);
      glyphs.push(new Glyph(font, info, position));
    }
    return glyphs;
  }
}
